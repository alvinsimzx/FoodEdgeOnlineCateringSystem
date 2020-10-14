from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UserRegisterForm
from accounts.models import InsertStock,InsertOrder,MenuItem,ActiveMenuItem
# Email Confirmation
from django.shortcuts import render
from django.core.mail import send_mail
import stripe

stripe.api_key = "sk_test_51HbjHmLUA515JZ27Y0RRePShcZS6VFq53mx0jiLs1DfdpRvA0YuyemAJWnhiI5Z0wNIwTZTaL3tngw9o2l0QMalz00lPtp37Mm"
# Create your views here.

def home(request):
    return render(request, 'accounts/index.html')
# Email Confirmation
def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        # send an email

        send_mail(
            'message from' +  message_name, # subject
            , # message
            , # from email
            ['desmondsim2222@gmail.com'], # To Email
        )

        return render(request, 'profile.html', {'message_name'})
    
    else:
        return render(request, 'profile.html', {})

def aboutUs(request):
    return render(request, 'accounts/AboutUs.html')

def StaffHome(request):
    return render(request, 'accounts/indexStaff.html')

def products(request):
    return render(request, 'accounts/products.html')

def customer(request):
    return render(request, 'accounts/customer.html')

def feedback(request):
    return render(request, 'accounts/feedback.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your accounts has been created! Please login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'accounts/register.html',{'form': form})

@login_required
def profile(request):
    allOrders = InsertOrder.objects.filter(customerID=request.user.id)
    return render(request, 'accounts/profile.html', {'allOrders' : allOrders})


def showStockPage(request):
    return render(request, 'accounts/StockManagementPage.html')

def ViewStocks(request):
    re = InsertStock.objects.all()
    return render(request, 'accounts/stock2.html', {'re': re})
    

def OrderMade(request):
    return render(request, 'accounts/ordermade.html')

def Payment(request):
    return render(request, 'accounts/CustomerPayment.html')

def charge(request):
    amount = 5
    if request.method == 'POST':
        print("Data:", request.POST)

        amount = int(request.POST['amount'])

        customer = stripe.Customer.create(
            email = request.POST['email'],
            name = request.POST['name'],
            source = request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer = customer,
            amount = amount*100,
            currency = 'myr',
            description = "CateringPayment"
        )
    
    return redirect(reverse('PaymentSuccess',args=[amount]))

def successMsg(request,args):
    amount = args
    return render(request,'accounts/PaymentSuccess.html',{'amount':amount})

def InsertCustomerOrder(request):
    if request.method =='POST':
        saverecord = InsertOrder()
        i = True
        if request.POST.get('CustFirstName'):
            saverecord.CustFirstName = request.POST.get('CustFirstName')
            saverecord.customerID = request.user.id
            saverecord.CustlastName = request.POST.get('CustlastName')
            saverecord.custEmail = request.POST.get('custEmail')
            saverecord.custContact = request.POST.get('custContact')
            saverecord.custOrder = request.POST.get('custOrder')
            saverecord.location = request.POST.get('location')
            saverecord.save()
            messages.success(request,'Order Sent')
            return render(request, 'accounts/order.html')
        else:
            messages.success(request,'Order did not send')
            return render(request, 'accounts/order.html')
    else:
        return render(request, 'accounts/order.html')

def Insertrecord(request):
    if request.method =='POST':
        if request.POST.get('stockName') and request.POST.get('amountLeft') and request.POST.get('deficit'):
            saverecord = InsertStock()
            saverecord.stockName=request.POST.get('stockName')
            saverecord.amountLeft=request.POST.get('amountLeft')
            saverecord.deficit=request.POST.get('deficit')
            saverecord.save()
            messages.success(request,'Record Saved')
            return render(request, 'accounts/stock.html')
    else:
        return render(request, 'accounts/stock.html')

def InsertMenu(request):
    re = InsertStock.objects.all()
    if request.method == 'POST':
        if request.POST.get('stockID') and request.POST.get('itemName') and request.POST.get('itemPrice'):
            saverecord = MenuItem()
            saverecord.stockID = request.POST.get('stockID')
            saverecord.itemName = request.POST.get('itemName')
            saverecord.itemPrice = request.POST.get('itemPrice')
            saverecord.save()
            messages.success(request,'Menu Item Saved')
            return render(request, 'accounts/menu.html', {'re': re})
    else:
         return render(request, 'accounts/menu.html', {'re': re})

def DeleteRecord(request, stockID):
    record = InsertStock.objects.get(stockID=stockID)
    record.delete()
    re = InsertStock.objects.all()
    return render(request, 'accounts/stock2.html', {'re': re})

def EditRecords(request, stockID):
     record = InsertStock.objects.get(stockID=stockID)
     if request.method =='POST':
        if request.POST.get('stockName') and request.POST.get('amountLeft') and request.POST.get('deficit'):
            record.stockName = request.POST.get('stockName')
            record.amountLeft = request.POST.get('amountLeft')
            record.deficit = request.POST.get('deficit')
            record.save()
            messages.success(request,'Record Edited')
            re = InsertStock.objects.all()
            return render(request, 'accounts/stock2.html', {'re': re}) 
     else:
        return render(request, 'accounts/editStock.html')

def ShowSets(request):
    AvailableItems = ActiveMenuItem.objects.all()
    return render(request, 'accounts/sets.html', {'AvailableItems' : AvailableItems})

def StaffLogin(request):
    return render(request, 'accounts/indexStaff.html')

def ShowGivenOrders(request):
    return render(request, 'accounts/CheckAssignedOrders.html')

def ShowAddMenuItems(request):
    return render(request, 'accounts/addMenuItems.html')

def ShowAssignOrdersToStaff(request):
    return render(request, 'accounts/AssignOrdersToStaff.html')
