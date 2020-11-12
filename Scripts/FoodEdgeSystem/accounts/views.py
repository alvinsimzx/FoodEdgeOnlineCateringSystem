from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,resolve,reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.views import generic
from django.utils.safestring import mark_safe
import os
import json

from django.http import JsonResponse,HttpResponse,HttpResponseRedirect

from .decorators import allowed_users
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,EventForm,EventMember,AddMemberForm,StockForm,StockImageEdit

from .models import *
from .utils import Calendar

from accounts.models import InsertStock,InsertOrder,MenuItem,InsertCustomer,StaffTable,StaffTeam

# Email Confirmation
from django.core.mail import send_mail
import stripe
# #Date and time picker
from django import forms
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from datetime import datetime
from datetime import timedelta
import calendar

from django.core import serializers

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
             # message# from email
            ['desmondsim2222@gmail.com'], # To Email
        )

        return render(request, 'profile.html', {'message_name'})
    
    else:
        return render(request, 'profile.html', {})

def aboutUs(request):
    return render(request, 'accounts/AboutUs.html')

def products(request):
    return render(request, 'accounts/products.html')

def customer(request):
    return render(request, 'accounts/customer.html')

def feedback(request):
    items = MenuItem.objects.all()
    if request.method == 'POST':
        saverecord = Comments()
        saverecord.menuItemID = request.POST.get('menuItemID')
        saverecord.rating = request.POST.get('rating')
        saverecord.commentfName = request.POST.get('commentfName')
        saverecord.commentlName = request.POST.get('commentlName')
        saverecord.commentContent = request.POST.get('commentContent')
        saverecord.save()
        messages.success(request, f'You have succesfully sent your feedback!')
    return render(request, 'accounts/feedback.html', {'items': items})

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
    allOrders = InsertOrder.objects.filter(customerID=request.user.id)
    allPayment = InsertCustomer.objects.get(authID=request.user.id)
    transactionInfo = []
    paymentInfo = {"brand":[],"last4":[]}
    paymentLength = len(paymentInfo)

    if request.method == 'POST':
        #Edit Option of the profile page
        #Profile form (request.FILES for images)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your accounts has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    if(stripe.PaymentMethod.list(customer=allPayment.customerID,type="card",)):
        for i in range(len(stripe.PaymentMethod.list(customer=allPayment.customerID,type="card",))):
            paymentInfo["brand"].append(stripe.PaymentMethod.list(customer=allPayment.customerID,type="card",)["data"][i]["card"]["brand"])
            paymentInfo["last4"].append(stripe.PaymentMethod.list(customer=allPayment.customerID,type="card",)["data"][i]["card"]["last4"])
        
    
    if(stripe.Charge.list(customer=allPayment.customerID,limit=3)):
        transactionInfo = {
            "amount":(stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["amount"]/100),
            "transaction_id":stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["balance_transaction"],
            "description":stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["description"],
            "brand": stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["source"]["brand"],
            "last4": stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["source"]["last4"],
            "exp_month":stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["source"]["exp_month"],
            "exp_year":stripe.Charge.list(customer=allPayment.customerID,limit=3)["data"][0]["source"]["exp_year"]
        }
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'allOrders' : allOrders,
        'paymentInfo':paymentInfo,
        'transactionInfo':transactionInfo
    }
    
    return render(request, 'accounts/profile.html', context)

def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, f'Password update successful!')
            return redirect('accounts-home')
        else:
            return redirect('changePassword')
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

@allowed_users(allowed_roles=['Operations'])
def customerAccounts(request):
    users = User.objects.all()
    return render(request, 'accounts/customerAccounts.html', {'users' : users})

def deleteCustomerAccount(request, username):
    account = User.objects.get(username=username)
    account.delete()
    users = User.objects.all()
    return redirect('CustomerAccounts')

def deleteCustomerAccountCustomer(request, username):
    account = User.objects.get(username=username)
    account.delete()
    users = User.objects.all()
    messages.success(request, f'Your accounts has been deleted!')
    return redirect('accounts-home')

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



def ShowAssignOrdersToStaff(request):
    record = InsertOrder.objects.filter(teamID__isnull=True)
    SearchedOrder = None
    teams = StaffTeam.objects.all()

    if request.method == 'POST':
        if request.POST.get('teamID') and (request.POST.get('submit') == "Submit"):
            print(request.POST.get('ChosenOrder'))
            update = InsertOrder.objects.get(orderID=request.POST.get('ChosenOrder'))
            update.teamID = request.POST.get('teamID')
            update.save()
            messages.success(request,'Order number #' + str(request.POST.get('ChosenOrder')) +   ' has been assigned to Team #' + str(request.POST.get('teamID')))
        elif request.POST.get('order'):
            SearchedOrder = InsertOrder.objects.filter(orderID=request.POST.get('order'))
       
    return render(request, 'accounts/AssignOrdersToStaff.html', {'records': record,'SearchedOrder':SearchedOrder, 'teams': teams})
    

def OrderMade(request):
    return render(request, 'accounts/ordermade.html')

def Payment(request,args):
    orderid = args
    paymentInfo = {"last4":[],"id":[]}
    if request.user.is_authenticated:
        allPayment = InsertCustomer.objects.get(authID=request.user.id)
        if(stripe.PaymentMethod.list(customer=allPayment.customerID,type="card",)):
            for i in range(len(stripe.PaymentMethod.list(customer=allPayment.customerID,type="card",))):
                paymentInfo["last4"].append(stripe.PaymentMethod.list(customer=allPayment.customerID,type="card",)["data"][i]["card"]["last4"])
                paymentInfo["id"].append(stripe.PaymentMethod.list(customer=allPayment.customerID,type="card",)["data"][i]["id"])
        allPayment = InsertCustomer.objects.get(authID=request.user.id)
        total = InsertOrder.objects.get(orderID=orderid).amountDue
    else:
        total = InsertOrder.objects.get(orderID=orderid).amountDue
    
    context={
        'total':total,
        'orderID':orderid,
        'allCustPayment':paymentInfo
        }
    return render(request, 'accounts/CustomerPayment.html',context)

def charge(request):
    if request.method == 'POST':
        print("Data:", request.POST)
        userid = ""
        
        orderid = request.POST['orderid']
        amount = InsertOrder.objects.get(orderID=orderid).amountDue

        if request.user.is_authenticated:
            allPayment = InsertCustomer.objects.get(authID=request.user.id)
            email = allPayment.email
            userid = allPayment.customerID
            if(request.POST['custPrevPayment']!="select"):
                charge = stripe.Charge.create(customer = allPayment.customerID,amount = amount*100,currency = 'myr',source=request.POST['custPrevPayment'],description = orderid)
                print("OK")
            else:
                source = stripe.Customer.create_source(allPayment.customerID,source=request.POST['stripeToken'])
                charge = stripe.Charge.create(customer = allPayment.customerID,amount = amount*100,currency = 'myr',description = orderid)
            
        else:
            customer = stripe.Customer.create(email = request.POST['email'],name = request.POST['name'],source = request.POST['stripeToken'])
            charge = stripe.Charge.create(customer = customer,amount = amount*100,currency = 'myr',description = "CateringPayment")  
            userid = customer.id

        return redirect(reverse('PaymentSuccess',args=[orderid]))
    else:
        return render(request,'accounts/PaymentSuccess.html')


def successMsg(request,args):
    orderid= args
    Orderinfo = InsertOrder.objects.get(orderID=orderid)
    return render(request,'accounts/PaymentSuccess.html',{'OrderInfo': Orderinfo})

# # Date and time picker
# class DTForm(forms.Form):
#     date_input = forms.DateField(widget=AdminDateWidget())
#     time_input = forms.DateField(widget=AdminTimeWidget())
#     # date_time_input = forms.DateField(widget=AdminSplitDateTime())

# def dtpicker(request):
#     form = DTForm()
#     return render(request, 'accounts/order.html', {'form':form})

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
            saverecord.custOrder = MenuItem.objects.get(menuItemID=int(request.POST.get('custOrder'))).itemName
            saverecord.custRequest = request.POST.get('custRequest')
            if request.user.is_authenticated:
                price = (MenuItem.objects.get(menuItemID=int(request.POST.get('custOrder'))).itemPrice)*0.9
                
            else:
                price = MenuItem.objects.get(menuItemID=int(request.POST.get('custOrder'))).itemPrice
            saverecord.amountDue = price
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
            messages.success(request,'Order Sent to our team')
            return redirect(reverse('Payment',args=[saverecord.orderID]))
        else:
            messages.success(request,'Order did not send')
            return redirect(reverse('Payment',args=[price]))
    else:
        MenuList = MenuItem.objects.all()
        return render(request, 'accounts/order.html',{'MenuList':MenuList})


def InsertMenu(request):
    re = InsertStock.objects.all()
    mn = MenuItem.objects.all()
    if request.method == 'POST':
        if request.POST.get('itemName') and request.POST.get('itemPrice'):
            for mns in mn:
                if(mns.itemName == request.POST.get('itemName')):
                    messages.warning(request, 'Same Item Detected')
                    return redirect('addMenuItems')
            saverecord = MenuItem()
            saverecord.itemName = request.POST.get('itemName')
            saverecord.itemPrice = request.POST.get('itemPrice')
            saverecord.save()
            messages.success(request,'Menu Item Saved')
            return redirect('addMenuItems')
    else:
         return render(request, 'accounts/menu.html', {'mn': mn})

def DeleteRecord(request, id):
    record = InsertStock.objects.get(id=id)
    record.delete()
    re = InsertStock.objects.all()
    return redirect('ViewStocks')

def ShowSets(request):
    re = InsertStock.objects.all()
    menu = MenuItem.objects.all()
    comments = Comments.objects.all()
    lowStock = []
    notAvailable = []
    menu1 = []
    menu2 = []
    menu3 = []
    for res in re:
        if(res.amountLeft <= 10):
            lowStock.append(res)
    for res in re: 
        if(res.menuItemID == menu[0].menuItemID):
            menu1.append(res)
    for res in re: 
        if(res.menuItemID == menu[1].menuItemID):
            menu2.append(res)
    for res in re: 
        if(res.menuItemID == menu[2].menuItemID):
            menu3.append(res)
    for item in lowStock:
        if(MenuItem.objects.get(menuItemID=item.menuItemID) not in notAvailable):
            notAvailable.append(MenuItem.objects.get(menuItemID=item.menuItemID))

    return render(request, 'accounts/sets.html', {'re': re, 'notAvailable' : notAvailable, 'menu': menu, 'comments': comments, 'menu1': menu1, 'menu2': menu2, 'menu3': menu3})

def ShowTransactions(request):
    return render(request, 'accounts/CustomerTransactions.html')

@allowed_users(allowed_roles=['Operations'])
def StaffHome(request):
    return render(request, 'accounts/indexStaff.html')

def StaffLogin(request):
    allowed_roles=['Operations']
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        print()

        if (user is not None) and (user.groups.filter(name='Operations').exists()):
            login(request,user)
            return redirect('staff-home')
        elif (user is not None) and (user.groups.filter(name='Management').exists()):
            login(request,user)
            return redirect('Management-home')
        else:
            messages.info(request,'You do not have the permission to log into this')

    return render(request, 'accounts/stafflogin.html')

@allowed_users(allowed_roles=['Operations'])
def ShowGivenOrders(request):
    UserTeamID = StaffTable.objects.get(staffID=request.user.id).teamID
    AssignedOrder = InsertOrder.objects.filter(teamID=UserTeamID)
    AssignedOrder = AssignedOrder.filter(Status=0)
    SearchedOrder = None

    if request.method == 'POST':
        if request.POST.get('markComplete')=="Mark as Complete":
            recordAsComplete = InsertOrder.objects.get(orderID=request.POST.get('SearchedID'))
            recordAsComplete.Status = 1
            recordAsComplete.save()
            messages.info(request,'Order #' + request.POST.get('SearchedID') + ' is marked as complete!')

        elif request.POST.get('order'):
            SearchedOrder = InsertOrder.objects.filter(orderID=request.POST.get('order'))

    return render(request, 'accounts/CheckAssignedOrders.html', {'AssignedOrder': AssignedOrder,'SearchedOrder':SearchedOrder})

@allowed_users(allowed_roles=['Operations'])
def ShowAddMenuItems(request):
    return render(request, 'accounts/addMenuItems.html')

# @allowed_users(allowed_roles=['Management'])
def dashboard_with_pivot(request):
    return render(request, 'accounts/profitBalance.html', {})

def dashboard_with_pivot2(request):
    return render(request, 'accounts/lossBalance.html', {})

def pivot_data(request):
    dataset = InsertOrder.objects.all()
    dataset2 = InsertStock.objects.all()
    data = serializers.serialize('json', dataset)
    data2 = serializers.serialize('json',dataset2)
    # trans = stripe.Charge.list(limit=3)["data"][0]
    # trans = stripe.Charge.list(limit=3)["data"][0]["amount"]
    # print(trans)
    return JsonResponse({'data':data, 'data2':data2}, safe=False)

@allowed_users(allowed_roles=['Management'])
def ManagementHome(request):
    return render(request, 'accounts/indexManagement.html')



class CalendarView(generic.ListView):
    model = Event
    template_name = 'accounts/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()


def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            id=request.user.id,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'accounts/event.html', {'form': form})

class EventEdit(generic.UpdateView):
    model = Event
    fields = ['title', 'description', 'start_time', 'end_time']
    template_name = 'accounts/event.html'


def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {
        'event': event,
        'eventmember': eventmember
    }
    return render(request, 'accounts/event-details.html', context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == 'POST':
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data['user']
                EventMember.objects.create(
                    event=event,
                    user=user
                )
                return redirect('calendar')
            else:
                print('--------------User limit exceed!-----------------')
    context = {
        'form': forms
    }
    return render(request, 'accounts/add_member.html', context)

class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = 'accounts/event_delete.html'
    success_url = reverse_lazy('calendar')

def Insertrecord(request):
    if request.method =='POST':
        form = StockForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.save() 
            messages.success(request,'Record Saved')
            return redirect('AddStocks')
        else:
            messages.warning(request,'Form is not valid')
            return render(request,'accounts/stock.html', {'form':form})
    else:
        form = StockForm()
        return render(request,'accounts/stock.html', {'form':form})

def EditRecords(request, id):
    mn = MenuItem.objects.all()
    record = InsertStock.objects.get(id=id)
    if request.method =='POST':
        if request.POST.get('stockName') and request.POST.get('menuItemID') and request.POST.get('amountLeft') and request.POST.get('deficit'):
            record.stockName = request.POST.get('stockName')
            record.menuItemID = request.POST.get('menuItemID')
            record.amountLeft = request.POST.get('amountLeft')
            record.deficit = request.POST.get('deficit')
            record.save()
            messages.success(request,'Record Edited')
            return redirect('ViewStocks')
    else:
        return render(request, 'accounts/editStock.html', {'mn': mn, 'record': record})

def EditStockImage(request, id):
    mn = MenuItem.objects.all()
    record = InsertStock.objects.get(id=id)
    previousImg = record.stockImage.path
    if request.method =='POST':
        form = StockImageEdit(request.POST, request.FILES, instance=record)
        if form.is_valid(): 
            os.remove(previousImg)
            form.save() 
            messages.success(request,'Image Edited')
            return redirect('ViewStocks')
        else:
            form = StockImageEdit()
            messages.warning(request,'Form is not valid')
            return render(request,'accounts/stockImageUpdate.html', {'record':record, 'form':form})
    else:
        form = StockImageEdit()
        return render(request,'accounts/stockImageUpdate.html', {'record':record, 'form':form})

def ProfitLoss(request):
    order = InsertOrder.objects.all()
    stock = InsertStock.objects.all()
    menu = MenuItem.objects.all()
    profitList = []
    lossList = []
    for i in order:
        profitList.append(i.amountDue)
    for j in stock:
        lossList.append(j.deficit)
    profit = sum(profitList)
    loss = sum(lossList)
    nett = profit - loss
    return render(request, 'accounts/profitloss.html', {'order':order, 'stock':stock, 'menu':menu, 'profit':profit, 'loss':loss, 'nett':nett})