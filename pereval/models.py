from django.db import models
from django.contrib.auth.models import AbstractUser


class Level(models.Model):
    winter = models.CharField(max_length=2, blank=True)
    summer = models.CharField(max_length=2, blank=True)
    autumn = models.CharField(max_length=2, blank=True)
    spring = models.CharField(max_length=2, blank=True)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Pereval(models.Model):
    STATUSES = {
        'NE': 'новый',
        'PE': 'ожидается',
        'AC': 'принято',
        'RE': 'отклонено'
    }

    add_time = models.DateTimeField()
    beauty_title = models.CharField(max_length=25)
    title = models.CharField(max_length=25)
    other_titles = models.CharField(max_length=25)
    connect = models.CharField(max_length=25, blank=True)
    status = models.CharField(max_length=8, choices=STATUSES, default='NE')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)


class Images(models.Model):
    data = models.CharField(max_length=320)
    title = models.CharField(max_length=50)
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=16)
    fam = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    otc = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
