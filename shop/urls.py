from django.urls import path
from . import views

urlpatterns = [
    path('',views.Homepage,name="home"),
    path('register/',views.register,name="register"),
    path('login/',views.Login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('collections/',views.Collections,name="collections"),
    path('collections/<str:name>',views.Collectionsview,name="collections"),
    path('collections/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('addcart/',views.addCart,name="addcart"),
    path('cart/', views.cart_view, name='cart'),
    path('download_cart_pdf/',views.download_cart_pdf, name='download_cart_pdf'),




]
