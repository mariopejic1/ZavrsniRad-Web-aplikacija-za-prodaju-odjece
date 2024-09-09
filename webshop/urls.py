from django.urls import path
from . import views

app_name = "webshop"

urlpatterns = [
    path('', views.home_view, name='home'),
    path('base/', views.base_view, name='base'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'), 
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('returns/', views.returns_view, name='returns'),
    path('payment/', views.payment_view, name='payment'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('personal_data/', views.personal_data_view, name='personal_data'),
    path('orders/', views.orders_view, name='orders'),
    path('<slug:category_name>/<slug:subcategory_name>/', views.articles_display_view, name='articles_display'),
    path('sort_articles/', views.sort_articles, name='sort_articles'),
    path('<slug:product_slug>/', views.articles_details_view, name='articles_details'),
]