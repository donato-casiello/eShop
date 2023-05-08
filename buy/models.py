from django.conf import settings
from django.db import models
from django.shortcuts import reverse
 
from django.contrib.auth.models import User
from django_countries.fields import CountryField


CATEGORY_CHOICES = (
    ('Wear', "Wear"),
    ('Digital Services', "Digital"),
    ('Cosmetic and Body Care', "Cosmetic"),
    ('Furniture and Decor', "Furniture"),
    ('Household Items', "Household"),
    ('Media', "Media"),
    ('Pet Care', "Pet"),
    ('Office equipment', "Office"),
)

LABEL_CHOICES = (
    ('primary', "New"),
    ('secondary', "Out of stock"),
    ('danger', "Sale"),
)

# The product
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    discount_price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=23)
    label = models.CharField(choices=LABEL_CHOICES, max_length=10) 
    slug = models.SlugField() 
    description = models.TextField()
    additional_information = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True)
    a_image1 = models.ImageField(blank=True)
    a_image2 = models.ImageField(blank=True)
    a_image3 = models.ImageField(blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
    def add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug": self.slug})
    
    def increaseQuantity_url(self):
        return reverse("increaseQuantity", kwargs={"slug": self.slug})
    
    def remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug": self.slug})


# An intermediate step between Item and Order 
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False) # The order was sent or not
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_price(self):
        return self.item.price * self.quantity

    def get_total_discount_price(self):
        return self.item.discount_price * self.quantity

    def get_amount_saved(self):
        return self.get_total_price() - self.get_total_discount_price() 
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_price()


# The cart
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True) # date of creation
    ordered_date = models.DateTimeField() # date of sent
    ordered = models.BooleanField(default=False) # The order was sent or not
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    #payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
    

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    cap = models.CharField(max_length=5)
    
    def __str__(self):
        return self.user.username
    

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    state = CountryField(multiple=False, blank=True, null=True)
    profile_image = models.ImageField(blank=True)
    
    def __str__(self):
        return self.user.username