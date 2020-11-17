from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Event,EventMember,MenuItem,InsertStock
from django.core.validators import RegexValidator

from django.forms import ModelForm, DateInput
# #Date and time picker
# from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta: 
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ['image']

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class DateForm(forms.Form):
    my_date_field = forms.DateField(widget=DateInput)

class TimeForm(forms.Form):
    my_time_field = forms.DateField(widget=TimeInput)


class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d,%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d,%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class SignupForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class AddMemberForm(forms.ModelForm):
  class Meta:
    model = EventMember
    fields = ['user']

class StockForm(forms.ModelForm):
  CHOICES = []
  menu = MenuItem.objects.all()
  for items in menu:
    CHOICES.append((items.menuItemID,items.itemName))
  menuItemID = forms.ChoiceField(choices=CHOICES)
  amountLeft = forms.IntegerField(max_value=9999)
  deficit = forms.IntegerField(max_value=99999)
  class Meta:
    model = InsertStock
    fields = ['stockName', 'amountLeft', 'deficit', 'stockImage', 'menuItemID']

class StockImageEdit(forms.ModelForm):
  class Meta: 
      model = InsertStock
      fields = ['stockImage']