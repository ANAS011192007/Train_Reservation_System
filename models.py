from django.db import models

# Create your models here.
class trains(models.Model):
    tid=models.IntegerField(default=1)
    train_name=models.CharField(max_length=50)
    source=models.CharField(max_length=50)
    destination=models.CharField(max_length=50)
    Coach=models.CharField(max_length=50)
    Seat=models.CharField(max_length=50)
    time=models.TimeField(auto_now=False, auto_now_add=False)
    price=models.FloatField(default=120)
    seats_available=models.IntegerField()
    datee=models.DateField(default="2022-06-11")
    status=models.CharField(max_length=50,default="y")


class person(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    date_and_time_of_booking=models.DateTimeField(auto_now_add=True)
    train=models.ForeignKey('trains', on_delete=models.CASCADE)
    pay_check=models.IntegerField(default=0)

class seats(models.Model):
    train_name=models.CharField(max_length=50)
    Seat=models.CharField(max_length=50)
    Coach=models.CharField(max_length=50)
    datee=models.DateField(default="2022-06-11")
    status=models.CharField(max_length=50,default="y")
