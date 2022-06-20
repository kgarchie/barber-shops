from django.db import models
from django.contrib.auth.models import User
import random


# Create your models here.

class Locations(models.Model):
    county = models.CharField(max_length=20)
    locale = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.locale


class Barber(models.Model):
    id_no = models.IntegerField()
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField()
    picture = models.FileField(null=True, blank=True)
    available = models.BooleanField(default=True)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cut(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Appointments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cut = models.ForeignKey(Cut, on_delete=models.CASCADE, default=1)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE,
                               default=random.randrange(Barber.objects.filter(available=True).count()))
    dye = models.BooleanField()
    sth = models.TextField(blank=True, null=True)
    locale = models.ForeignKey(Locations, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.user.username
