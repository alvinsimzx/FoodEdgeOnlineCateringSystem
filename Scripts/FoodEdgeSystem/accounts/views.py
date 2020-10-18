from django.shortcuts import render,redirect
from django.urls import reverse,resolve
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
from .decorators import allowed_users
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from accounts.models import InsertStock,InsertOrder,MenuItem,ActiveMenuItem,InsertCustomer
# Email Confirmation
from django.shortcuts import render
from django.core.mail import send_mail
import stripe

stripe.api_key = "sk_test_51HbjHmLUA515JZ27Y0RRePShcZS6VFq53mx0jiLs1DfdpRvA0YuyemAJWnhiI5Z0wNIwTZTaL3tngw9o2l0QMalz00lPtp37Mm"
# Create your views here.

def home(request):
    return render(request, 'accounts/index.html')

def aboutUs(request):
    return render(request, 'accounts/AboutUs.html')

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
            customer1 = stripe.Customer.create(
                email = form.cleaned_data.get('email'),
                name = form.cleaned_data.get('username')
                )
            
            customerID = customer1.id 
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            createCustomer(request,customerID,user.id,username,form.cleaned_data.get('email'))

            messages.success(request, f'Your accounts has been created! Please login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'accounts/register.html',{'form': form})

def createCustomer(request,customerID,authID,username,email):
    saverecords = InsertCustomer()
    saverecords.customerID = customerID
    saverecords.authID = authID
    saverecords.name = username
    saverecords.email = email
    saverecords.save() 

@login_required
def profile(request):
    #Edit Option of the profile page
    u_form = UserUpdateForm()
    p_form = ProfileUpdateForm()

    allOrders = InsertOrder.objects.filter(customerID=request.user.id)
    allPayment = InsertCustomer.objects.get(authID=request.user.id)
    transactionInfo = []
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'allOrders' : allOrders,
        'transactionInfo':transactionInfo
    }
   


    if(stripe.Charge.list(customer=allPayment.customerID,limit=3)):
        transactionInfo = {
            "amount":stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["amount"],
            "transaction_id":stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["balance_transaction"],
            "description":stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["description"],
            "brand": stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["source"]["brand"],
            "last4": stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["source"]["last4"],
            "exp_month":stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["source"]["exp_month"],
            "exp_year":stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["source"]["exp_year"]
        }
    
    return render(request, 'accounts/profile.html', context)


def customerAccounts(request):
    users = User.objects.all()
    return render(request, 'accounts/customerAccounts.html', {'users' : users})

def deleteCustomerAccount(request, username):
    account = User.objects.get(username=username)
    account.delete()
    users = User.objects.all()
    return redirect('CustomerAccounts')

def showStockPage(request):
    return render(request, 'accounts/StockManagementPage.html')

def ViewStocks(request):
    re = InsertStock.objects.all()
    lowStock = []
    for res in re:
        if(res.amountLeft <= 10):
            lowStock.append(res)
    if(len(lowStock) != 0):
        messages.warning(request,'!!!Low stock detected!!!')
        messages.warning(request,'Low Stocks Displayed')

    return render(request, 'accounts/stock2.html', {'re': re, 'lowStock': lowStock})
    

def OrderMade(request):
    return render(request, 'accounts/ordermade.html')

def Payment(request,args):
    total = args
    return render(request, 'accounts/CustomerPayment.html',{'total':total})

def charge(request):
    if request.method == 'POST':
        print("Data:", request.POST)
        userid = ""
        
        amount = int(request.POST['amount'])

        if request.user.is_authenticated:
            allPayment = InsertCustomer.objects.get(authID=request.user.id)
            email = allPayment.email
            userid = allPayment.customerID
            source = stripe.Customer.create_source(allPayment.customerID,source=request.POST['stripeToken'])
            charge = stripe.Charge.create(customer = allPayment.customerID,amount = amount*100,currency = 'myr',description = "CateringPayment")
            #sends automated email to users
            
        else:
            customer = stripe.Customer.create(email = request.POST['email'],name = request.POST['name'],source = request.POST['stripeToken'])
            charge = stripe.Charge.create(customer = customer,amount = amount*100,currency = 'myr',description = "CateringPayment")  
            userid = customer.id

        return redirect('order')
    else:
        return redirect('order')


def successMsg(request,args):
    amount = args
    return render(request,'accounts/PaymentSuccess.html',{'amount':amount})

def InsertCustomerOrder(request):
    if request.method =='POST':
        saverecord = InsertOrder()
        if request.POST.get('CustFirstName') and request.POST.get('custLastName'):
            if(request.user.id != None):
                saverecord.customerID = request.user.id
            else:
                saverecord.customerID = 0
            saverecord.CustFirstName = request.POST.get('CustFirstName')
            saverecord.custLastName = request.POST.get('custLastName')
            saverecord.custEmail = request.POST.get('custEmail')
            saverecord.custContact = request.POST.get('custContact')
            saverecord.custOrder = request.POST.get('custOrder')
            saverecord.custRequest = request.POST.get('custRequest')
            price = int(request.POST.get('custOrder'))
            saverecord.location = request.POST.get('location')
            saverecord.save()
            send_mail(
                "FoodEdge Catering Payment Confirmation", 
                """
Thank you {} for ordering with FoodEdge Catering,
                \n
Your order is valued at {}. 
                \n
If you have not placed an order and received this email or have some other enquires, please send an email to foodedgecateringassignment@gmail.com, and we will clear things up shortly.
                \n
Regards,
FoodEdge Customer Service Team 
                \n
This is an auto-generated email, please send a new email instead of replying. 
                """.format(request.POST.get('custLastName'), request.POST.get('custOrder')), #message
                "foodedgecateringassignment@gmail.com", 
                [request.POST.get('custEmail')]
            )
            messages.success(request,'Order Sent')
            return redirect(reverse('Payment',args=[price]))
        else:
            messages.success(request,'Order did not send')
            return redirect(reverse('Payment',args=[price]))
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
    return redirect('ViewStocks')

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
            return redirect('ViewStocks')
     else:
        return render(request, 'accounts/editStock.html')

def ShowSets(request):
    AvailableItems = ActiveMenuItem.objects.all()
    return render(request, 'accounts/sets.html', {'AvailableItems' : AvailableItems})

def ShowTransactions(request):
    return render(request, 'accounts/CustomerTransactions.html')

@allowed_users(allowed_roles=['Operations'])
def StaffHome(request):
    return render(request, 'accounts/indexStaff.html')

def StaffLogin(request):
    allowed_roles=['c']
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        print()

        if (user is not None) and (user.groups.filter(name='Operations').exists()):
            login(request,user)
            return redirect('staff-home')
        else:
            messages.info(request,'You do not have the permission to log into this')

    return render(request, 'accounts/stafflogin.html')

@allowed_users(allowed_roles=['Operations'])
def ShowGivenOrders(request):
    return render(request, 'accounts/CheckAssignedOrders.html')

@allowed_users(allowed_roles=['Operations'])
def ShowAddMenuItems(request):
    return render(request, 'accounts/addMenuItems.html')

@allowed_users(allowed_roles=['Operations'])
def ShowAssignOrdersToStaff(request):
    return render(request, 'accounts/AssignOrdersToStaff.html')
