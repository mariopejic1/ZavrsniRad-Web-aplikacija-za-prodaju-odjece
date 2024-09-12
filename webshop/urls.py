from django.urls import path
from . import views

app_name = "webshop"

urlpatterns = [
    path('', views.female_homepage_view, name='female_homepage'),
    path('base/', views.base_view, name='base'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'), 
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('returns/', views.returns_view, name='returns'),
    path('payment/', views.payment_view, name='payment'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('personal_data/', views.personal_data_view, name='personal_data'),
    path('female_homepage/', views.female_homepage_view, name='female_homepage'),
    path('male_homepage/', views.male_homepage_view, name='male_homepage'),
    path('create_order/', views.create_order_view, name='create_order'),
    path('orders_history/', views.orders_history_view, name='orders_history'),
    path('order_details/<int:order_id>/', views.order_details_view, name='order_details'),
    path('<slug:category_name>/<slug:subcategory_name>/', views.articles_display_view, name='articles_display'),
    path('<slug:category_name>/<slug:subcategory_name>/sort_articles/', views.sort_articles, name='sort_articles'),
    path('<slug:category_name>/<slug:subcategory_name>/<slug:product_slug>/<slug:color>/', views.articles_details_view, name='articles_details'),    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('<slug:category_name>/<slug:subcategory_name>/<slug:product_slug>/<slug:color>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('search/', views.search_view, name='search'),   
    
]