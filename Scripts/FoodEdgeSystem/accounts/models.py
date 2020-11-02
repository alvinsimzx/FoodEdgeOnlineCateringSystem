
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime   
from PIL import Image
from django.dispatch import receiver 
from django.db.models.signals import post_save

# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width>300:
            output_Size = (300,300)
            img.thumbnail(output_Size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class InsertCustomer(models.Model):
    customerID = models.CharField(max_length=20,primary_key=True)
    authID = models.IntegerField()
    phoneNo = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    class Meta:
        db_table = "customer"


class InsertStock(models.Model):
    stockID = models.IntegerField(primary_key=True)
    stockName = models.CharField(max_length=100)
    amountLeft = models.IntegerField()
    deficit = models.IntegerField()
    menuItemID = models.IntegerField()
    class Meta:
        db_table = "Stock"
        
class MenuItem(models.Model):
    menuItemID = models.IntegerField(primary_key=True)
    itemName = models.CharField(max_length=100)
    itemPrice = models.IntegerField()
    class Meta:
        db_table = "menuitem"

class ActiveMenuItem(models.Model):
    activeItemID = models.IntegerField(primary_key=True)
    menuItemID = models.IntegerField()
    rating = models.IntegerField()
    class Meta:
        db_table = "activemenuitems"


class InsertOrder(models.Model):
    orderID = models.AutoField(primary_key=True)	
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


class StaffTable(models.Model):
    staffID = models.IntegerField(primary_key=True)	
    teamID = models.IntegerField()
    name = models.CharField(max_length=255)
    salary = models.IntegerField()
    class Meta:
        db_table = "staff"