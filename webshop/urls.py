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
]