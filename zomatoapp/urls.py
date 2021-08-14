from django.urls import path
from . import views
from django.conf.urls.static import static
from zomato.settings import MEDIA_URL,MEDIA_ROOT

urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('search/',views.search,name="search"),
    path('resturant/<int:resturantid>',views.detail,name="detail"),
    path('searchresturant/',views.searchresturant,name="searchresturant"),
    path('resturant/buy/<int:dish_id>',views.buy,name="buy"),
    path('payment/verify',views.verifypayment,name="paymentverify"),
    path('orders',views.orders,name="orders")

] + static(MEDIA_URL,document_root=MEDIA_ROOT)