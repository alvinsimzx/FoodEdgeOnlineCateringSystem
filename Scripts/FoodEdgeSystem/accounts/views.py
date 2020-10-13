from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from accounts.models import InsertStock,InsertOrder,MenuItem,ActiveMenuItem

# Create your views here.

def home(request):
    return render(request, 'accounts/index.html')

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
    lowStock = []
    for res in re:
        if(res.amountLeft <= 10):
            lowStock.append(res.stockID)
    if(len(lowStock) != 0):
        messages.warning(request,'Low stock detected')
        messages.warning(request, 'Low Stock IDs: {}'.format(str(lowStock).strip('[]')))

    return render(request, 'accounts/stock2.html', {'re': re})
    

def OrderMade(request):
    return render(request, 'accounts/ordermade.html')

'''
def CreateAccount(request):
    if request.method =='POST':
        if request.POST.get('CustomerName') and request.POST.get('phoneNo') and request.POST.get('email') and request.POST.get('username') and request.POST.get('password'):
            saverecord = InsertCustomer()
            saverecord.name=request.POST.get('CustomerName')
            saverecord.phoneNo=request.POST.get('phoneNo')
            saverecord.email=request.POST.get('email')
            saverecord.save()

            saveAccount = InsertAccount()
            saveAccount.customerID = saverecord.pk
            saveAccount.username = request.POST.get('username')
            saveAccount.accountPassword = request.POST.get('password')
            saveAccount.save()

            messages.success(request,'Account Created! Please Login')
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/register.html')
'''

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
            messages.warning(request,'Order did not send')
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

def StaffLogin(request):
    return render(request, 'accounts/indexStaff.html')

def ShowGivenOrders(request):
    return render(request, 'accounts/CheckAssignedOrders.html')

def ShowAssignOrdersToStaff(request):
    return render(request, 'accounts/AssignOrdersToStaff.html')
