import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import CheckoutForm, EditProfileForm

from .models import Item, OrderItem, Order, BillingAddress, Account

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET




# Home view
class HomeView(ListView):
    model = Item 
    paginate_by = 10
    template_name = "buy/home.html"
    
# Product detail
class ProductDetailView(DetailView):
    model = Item
    template_name = "buy/product_detail.html"

# Category view
def categoryList(request, category):
    object_list = Item.objects.filter(category=category)
    context = {
        "object_list" : object_list,
        "category" : category,
    }
    return render(request, "buy/category.html", context)

# Add item to cart
@login_required
def addToCart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False) 
    # Filter the Order objects to check if the user hasn't already send the order
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect('order-summary')
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect('order-summary')
    else:
        ordered_date = datetime.datetime.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('order-summary')
    
# Remove item from cart
@login_required
def removeFromCart(request, slug):
    item = get_object_or_404(Item, slug=slug)# Filter the Order objects to check if the user hasn't already send the order
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # Check if an order exists
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, 
                user=request.user, 
                ordered=False
            )[0] 
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect('order-summary')
        else: 
            messages.info(request, "This item was not in your cart.")
            return redirect('product_detail', slug=slug)    
    else:
        messages.info(request, "You don't have an active order.")
        return redirect('product_detail', slug=slug)
  
# Remove single item from cart  
@login_required
def removeSingleItemFromCart(request, slug):
    item = get_object_or_404(Item, slug=slug)# Filter the Order objects to check if the user hasn't already send the order
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # Check if an order exists
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, 
                user=request.user, 
                ordered=False)[0] 
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save() 
            else:
                order.items.remove(order_item)
            return redirect('order-summary')
        else: 
            messages.info(request, "This item was not in your cart.")
            return redirect('product_detail', slug=slug)    
    else:
        messages.info(request, "You don't have an active order.")
        return redirect('product_detail', slug=slug)
   
# Order summary 
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *arg, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = { 
                "object":order
                }
            return render(self.request, "buy/order_summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")
            return redirect("/")
        
# Profile page
class profilePage(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        # Account already exists
        try:
            account = Account.objects.get(user=self.request.user)
            initial_data = {
                "profile_image" : account.profile_image,
                "first_name" : account.first_name,
                "last_name" : account.last_name,
                "mobile_number" : account.mobile_number,
                "address" : account.address,
                "birthday" : account.birthday,
                "state" : account.state,
            }
            form = EditProfileForm(initial=initial_data)
            context = {
                "form" : form,
                "account" : account,
                }
            return render(self.request, "buy/profile.html", context)
        # Account doesn't exists
        except ObjectDoesNotExist:
            form = EditProfileForm()
            context = {
                "form" : form,
                }
        return render(self.request, "buy/profile.html", context)
        
    
    def post(self, *args, **kwargs):
        form = EditProfileForm(self.request.POST or None, self.request.FILES or None)
        # Get the data from edit profile form
        if form.is_valid():
            print("FORM IS VALID")
            # User already has an account
            try:
                print("ACCOUNT EXISTS")
                account = Account.objects.get(user=self.request.user)
                # Update profile image
                if form.cleaned_data["profile_image"] != None:
                    account.profile_image = form.cleaned_data["profile_image"]
                else:
                    account.profile_image = account.profile_image
                account.first_name = form.cleaned_data.get("first_name")
                account.last_name = form.cleaned_data.get("last_name")
                account.mobile_number = form.cleaned_data.get("mobile_number")
                account.address = form.cleaned_data.get("address")
                account.state = form.cleaned_data.get("state")
                account.birthday = form.cleaned_data.get("birthday")
                account.save()
                print("ACCOUNT UPDATE")
                messages.success(self.request, "Profile updated correctly")
                return redirect("profile", username=self.request.user.username)
            # User doesn't has an account
            except ObjectDoesNotExist:
                print("ACCOUNT DOESN'T EXISTS")
                profile_image = form.cleaned_data["profile_image"]
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                mobile_number = form.cleaned_data.get("mobile_number")
                address = form.cleaned_data.get("address")
                state = form.cleaned_data.get("state")
                birthday = form.cleaned_data.get("birthday")
                # Create new account 
                new_account = Account(
                    user = self.request.user, 
                    profile_image = profile_image, 
                    first_name = first_name, 
                    last_name = last_name, 
                    mobile_number = mobile_number,
                    address = address, 
                    state = state, 
                    birthday = birthday
                )
                new_account.save()
                messages.success(self.request, "Profile updated correctly")
                return redirect("profile", username=self.request.user.username)
        else:
            messages.error(self.request, "Something went wrong")
            return redirect("profile", username=self.request.user.username)
        
# Checkout session to handle payment with stripe

class Create_Checkout_Session(LoginRequiredMixin, View):

    def post(self, *args, **kwargs):
        order_id = self.request.POST.get('order-id')
        order = Order.objects.get(user=self.request.user, id=order_id)
        host = self.request.get_host()
        host = self.request.get_host()
        print(order.get_total())
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ["card"],
                    line_items=[
                        {
                            "price_data" : {
                                "currency" : "eur",
                                "unit_amount" : int(order.get_total()) * 100,
                                "product_data" : {
                                    "name" : order.id,
                                }
                                },
                            "quantity" : 1,
                        }
                    ],
                    mode='payment',
                    success_url="http://{}{}".format(host, reverse(success)),
                    cancel_url="http://{}{}".format(host, reverse(cancel)),
                )
        return redirect(checkout_session.url, code=303)

    def get(self, *args, **kwargs):
            order = Order.objects.get(user=self.request.user, ordered=False)
            # Form
            form = CheckoutForm()
            context = {
                "form" : form,
                "order" : order,
            }
            return render(self.request, 'buy/checkout.html', context)

def success(request):
    context = {
        "payment_status" : 'success'
        }
    return render(request, "buy/success.html", context)

def cancel(request):
    context = {
        "payment_status" : 'cancel'
        }
    return render(request, "buy/cancel.html", context)


@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
    session = stripe.checkout.Session.retrieve(
      event['data']['object']['id'],
      expand=['line_items'],
    )

    if session.payment_status == "paid":
        # Fulfill the purchase...
        line_items = session.list_line_items(session.id, limit=1).data[0]
        order_id = line_items['description']
        fulfill_order(order_id)

  # Passed signature verification
  return HttpResponse(status=200)

def fulfill_order(order_id):
    print("RUN FULFILL FUNCTION")
    order = Order.objects.get(id=order_id)
    ordered_items = order.items.all()
    for item in ordered_items:
        item.ordered = True
        item.save()
    order.ordered = True
    order.ordered_date = datetime.datetime.now()
    order.save()