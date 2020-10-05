from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='accounts-home'),
    path('products/', views.products),
    path('customer/', views.customer),
    path('register/', views.register,name='register'),
]