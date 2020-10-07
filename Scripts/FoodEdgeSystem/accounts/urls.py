from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='accounts-home'),
    path('products/', views.products),
    path('customer/', views.customer),
    path('register/',views.register,name='register'),
    path('feedback/', views.feedback,name='feedback'),
    path('stock/',views.Insertrecord),
    path('stock2/', views.showStockPage2),
    path('menu/', views.InsertMenu), 
    path('sets/',views.ShowSets,name='sets'),
    path('order/',views.Order,name='order'),
    path('delete/<int:stockID>', views.DeleteRecord), 
    path('edit/<int:stockID>', views.EditRecords),
]