from django.db import models
from django.contrib.auth.models import User

class GiftCategory(models.Model):
    category_name = models.CharField(max_length=50)
    lower_price = models.IntegerField()
    higher_price = models.IntegerField()

    def __str__(self):
        return self.category_name

class Gift(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    category = models.ForeignKey(GiftCategory, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=50, null=True)
    point = models.IntegerField(null=True)
    role = models.IntegerField(default='2')
    total_spend = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class VendorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=50, null=True)
    org_name= models.CharField(max_length=50)
    role = models.IntegerField(default='1')

    def __str__(self):
        return self.name

#for admin <-----
class FeaturedAdCategory(models.Model):
    category_name = models.CharField(max_length=50, null=True)
    running_days = models.IntegerField(null=True)
    priority = models.IntegerField(null=True)
#----->

class FeaturedAd(models.Model):
    category = models.ForeignKey(FeaturedAdCategory ,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, null=True)
    ad_name = models.CharField(max_length=50)

class Qr(models.Model):
    qrscanned = models.BooleanField(default=False)
