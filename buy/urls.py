from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("product_detail/<slug>", views.ProductDetailView.as_view(), name="product_detail"),
    path("category/<str:category>/", views.categoryList, name="category"),
    path("search", views.search, name="search"),
    path("add-to-cart/<slug>", views.addToCart, name="add-to-cart"),
    path("remove-from-cart/<slug>", views.removeFromCart, name="remove-from-cart"),
    path("remove-single-item-from-cart/<slug>", views.removeSingleItemFromCart, name="remove-single-item-from-cart"),
    path("order-summary", views.OrderSummaryView.as_view(), name="order-summary"),
    #path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("create_checkout_session/", views.Create_Checkout_Session.as_view(), name="create_checkout_session"),
    path("profile/<str:username>/", views.profilePage.as_view(), name="profile"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    path("webhook/stripe", views.my_webhook_view, name="my_webhook_view"),
    ]