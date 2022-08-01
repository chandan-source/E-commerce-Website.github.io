
from django.contrib import admin
from django.urls import path
from shopping.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('contactus/',contactus,name='contact'),
    path('login/', logIn, name='login'),
    path('aboutus/', aboutus, name='about'),
    path('signin/', signup, name='sign'),
    path('logout/', Logout, name='logout'),
    path('shop/<int:sid>/',shop,name='Shop'),
    path('product/<int:pid>/',Product,name='product'),
    path('add_to_cart/<int:pid>/',addtocart,name='add_to_cart'),
    path('mycart/',mycart,name='mycart'),
    path('remove_product/<int:cid>/',remove_pro_from_cart,name='remove_product'),
    path('checkout/<str:cid>/',checkout,name="checkout"),
    path('payment_check/<int:order_id>/',payment_check,name="payment_check"),
    path('dashboard/<str:type>/',user_dashboard,name='dashboard'),
    path('track/<int:oid>/',track_order,name='track'),
    path('add_product/', add_product, name='add_product'),
    path('add_category/', add_category, name='add_category'),
    path('add_subcategory/', add_subcategory, name='add_subcategory'),
    path('order_details/<str:type>/',order_detail,name='order_detail'),
    path('change_status/<int:order_id>/',change_status,name='change_status'),
    path('delete/<str:type>/<int:did>', delete, name='delete'),
    path('edit/<str:type>/<int:eid>', edit, name='edit'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
