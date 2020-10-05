from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def home(request):
    return render(request, 'accounts/dashboard.html')

def products(request):
    return render(request, 'accounts/products.html')


def customer(request):
    return render(request, 'accounts/customer.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('accounts-home')
    else:
        form = UserRegisterForm()
    return render(request,'accounts/register.html',{'form': form})
