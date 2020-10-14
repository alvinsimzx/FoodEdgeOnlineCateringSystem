from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='accounts-home'),
    path('about/', views.aboutUs, name='AboutUs'),
    path('staffHome/', views.StaffHome, name='staff-home'),
    path('products/', views.products),
    path('customer/', views.customer),
    path('register/',views.register,name='register'),
    path('feedback/', views.feedback,name='feedback'),
    path('stockManagement/',views.showStockPage, name="stock"),
    path('AddStocks/',views.Insertrecord, name="AddStocks"),
    path('viewStocks/', views.ViewStocks, name="ViewStocks"),
    path('menu/', views.InsertMenu,name='addMenuItems'), 
    path('sets/',views.ShowSets,name='sets'),
    path('order/',views.InsertCustomerOrder,name='order'),
    path('StaffLogin/',views.StaffLogin,name='StaffLogin'),
    path('Payment/',views.Payment, name='Payment'),
    path('charge/',views.charge, name="charge"),
    path('success/<str:args>/',views.successMsg,name="PaymentSuccess"),
    path('CheckAssignedOrders/',views.ShowGivenOrders,name='CheckAssignedOrders'),
    path('addMenuItems/',views.ShowAddMenuItems,),
    path('AssignOrdersToStaff/',views.ShowAssignOrdersToStaff,name='AssignOrdersToStaff'),
    path('delete/<int:stockID>', views.DeleteRecord), 
    path('edit/<int:stockID>', views.EditRecords),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)