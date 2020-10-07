from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from accounts.models import InsertStock
from accounts.models import MenuItem

# Create your views here.

def home(request):
    return render(request, 'accounts/dashboard.html')

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
    return render(request, 'accounts/profile.html')

def showStockPage(request):
    return render(request, 'accounts/stock.html')

def showStockPage2(request):
    re = InsertStock.objects.all()
    return render(request, 'accounts/stock2.html', {'re': re})
    
def Order(request):
    return render(request, 'accounts/order.html')

def OrderMade(request):
    return render(request, 'accounts/ordermade.html')

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
            saverecord.stockID = InsertStock.objects.get(stockID = request.POST.get('stockID'))
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
    return render(request, 'accounts/sets.html')