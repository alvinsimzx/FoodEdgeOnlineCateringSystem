from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

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