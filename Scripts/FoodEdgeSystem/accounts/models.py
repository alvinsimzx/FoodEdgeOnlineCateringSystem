from django.urls import reverse
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

class Comments(models.Model):
    commentID = models.IntegerField(primary_key=True)
    menuItemID = models.IntegerField()
    rating = models.IntegerField()
    commentfName = models.CharField(max_length=100)
    commentlName = models.CharField(max_length=100)
    commentContent = models.CharField(max_length=255)
    class Meta:
        db_table = "comments"


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
    Status = models.BooleanField()
    class Meta:
        db_table = "cateringorder"	 	


class StaffTable(models.Model):
    staffID = models.IntegerField(primary_key=True)	
    teamID = models.IntegerField()
    name = models.CharField(max_length=255)
    salary = models.IntegerField()
    class Meta:
        db_table = "staff"

class StaffTeam(models.Model):
    teamID = models.IntegerField(primary_key = True)
    dateFormed = models.DateField()
    dateDisbanded = models.DateField()
    class Meta:
        db_table = "staffteam" 

class Event(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('event-detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

class EventMember(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return str(self.user)