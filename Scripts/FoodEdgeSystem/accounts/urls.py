from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
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
    path('order/',views.InsertCustomerOrder,name='order'),
    path('StaffLogin/',views.StaffLogin,name='StaffLogin'),
    path('CheckAssignedOrders/',views.ShowGivenOrders,name='CheckAssignedOrders'),
    path('addMenuItems/',views.ShowAddMenuItems,name='addMenuItems'),
    path('AssignOrdersToStaff/',views.ShowAssignOrdersToStaff,name='AssignOrdersToStaff'),
    path('delete/<int:stockID>', views.DeleteRecord), 
    path('edit/<int:stockID>', views.EditRecords),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)