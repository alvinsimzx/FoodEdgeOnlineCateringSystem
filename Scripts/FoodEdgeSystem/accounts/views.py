from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from accounts.models import InsertStock

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

def ShowSets(request):
    return render(request, 'accounts/sets.html')