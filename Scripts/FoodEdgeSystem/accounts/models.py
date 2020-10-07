
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    

# Create your models here.

class Profile (models.Model):
    def __str__(self):
        return f'{self.user.username} Profile'

'''
class InsertCustomer(models.Model):
    CustomerID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phoneNo = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    class Meta:
        db_table = "customer"

class InsertAccount(models.Model):
    accountID = models.IntegerField(primary_key=True)
    CustomerID = models.IntegerField()
    username = models.CharField(max_length=100)
    accountPassword = models.CharField(max_length=30)
    class Meta:
        db_table = "account"
'''
class InsertStock(models.Model):
    stockID = models.IntegerField(primary_key=True)
    stockName = models.CharField(max_length=100)
    amountLeft = models.IntegerField()
    deficit = models.IntegerField()
    class Meta:
        db_table = "Stock"
        
class MenuItem(models.Model):
    menuItemID = models.IntegerField(primary_key=True)
    stockID = models.ForeignKey(InsertStock, on_delete=models.CASCADE) #Issue is here, something about the column does not exist
    itemName = models.CharField(max_length=100)
    itemPrice = models.IntegerField()
    class Meta:
        db_table = "menuitem"

class InsertOrder(models.Model):
    orderID = models.IntegerField(primary_key=True)	
    teamID 	= models.IntegerField()
    customerID = models.IntegerField()
    cateringDatetime = models.DateTimeField(default=datetime.now, blank=True)	
    CustFirstName =	models.CharField(max_length=255)
    custLastName = models.CharField(max_length=255)	
    custEmail =	models.CharField(max_length=50)
    custContact = models.CharField(max_length=20)	
    custOrder = models.CharField(max_length=255)	 	
    custRequest = models.CharField(max_length=255)	 	
    location = models.CharField(max_length=255)	 	
    amountDue = models.IntegerField(default="50")
    class Meta:
        db_table = "cateringorder"	 	