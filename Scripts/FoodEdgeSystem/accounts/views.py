from django.shortcuts import render,redirect
from django.contrib import messages
from accounts.models import StockInsert
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

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

def Insertrecord(request):
    if request.method == 'POST':
        if request.POST.get('stockname') and request.POST.get('currentAmount') and request.POST.get('pricing'):
            saverecord = StockInsert()
            saverecord.stockName = request.POST.get('stockname')
            saverecord.amountLeft = request.POST.get('currentAmount')
            saverecord.deficit = request.POST.get('pricing')
            saverecord.save()
            messages.succes(request, 'record saved')
            return render(request, 'accounts/dashboard.html')
        else:
            return render(request, 'accounts/products.html')