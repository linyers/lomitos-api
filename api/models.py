from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()


def lomito_directory_path(instance, filename):
    logo = 'lomitos/{0}/logo.jpg'.format(instance.name)
    full_path = os.path.join(settings.MEDIA_ROOT, logo)

    if os.path.exists(full_path):
        os.remove(full_path)

    return logo


class DayTime(models.Model):
    sunday = models.CharField(max_length=11, null=True, blank=True)
    monday = models.CharField(max_length=11, null=True, blank=True)
    tuesday = models.CharField(max_length=11, null=True, blank=True)
    wednesday = models.CharField(max_length=11, null=True, blank=True)
    thursday = models.CharField(max_length=11, null=True, blank=True)
    friday = models.CharField(max_length=11, null=True, blank=True)
    saturday = models.CharField(max_length=11, null=True, blank=True)


class NightTime(models.Model):
    sunday = models.CharField(max_length=11, null=True, blank=True)
    monday = models.CharField(max_length=11, null=True, blank=True)
    tuesday = models.CharField(max_length=11, null=True, blank=True)
    wednesday = models.CharField(max_length=11, null=True, blank=True)
    thursday = models.CharField(max_length=11, null=True, blank=True)
    friday = models.CharField(max_length=11, null=True, blank=True)
    saturday = models.CharField(max_length=11, null=True, blank=True)


class Rating(models.Model):
    rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    reviews = models.IntegerField(null=True, blank=True)


class Lomito(models.Model):
    name = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=15, null=True)
    maps = models.URLField(null=True)
    logo = models.ImageField(upload_to=lomito_directory_path, null=True)
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE,blank=True, null=True)
    day_time = models.OneToOneField(DayTime, on_delete=models.CASCADE,blank=True, null=True)
    night_time = models.OneToOneField(NightTime, on_delete=models.CASCADE,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name