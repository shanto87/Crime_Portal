from Crime_Portal.settings import TIME_ZONE
from django.db import models

# Create your models here.


class Authentication(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    usertype = models.CharField(max_length=50)


class Registered_Users(models.Model):
    email = models.CharField(max_length=50)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    nid = models.CharField(max_length=100)
    image = models.FileField(upload_to='uploaded_images/')

    def __str__(self):
        return self.email


class WantedCriminals(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='criminal_images/')


class GeneralDiary(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    nid = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    issuedate = models.DateField()
    issuetime = models.TimeField()
    gdtype = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    psname = models.CharField(max_length=100)
    subject = models.CharField(max_length=300)
    details = models.TextField()
    gd_id = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)



class GeneralDiaryByUsers(models.Model):
    email = models.CharField(max_length=100)
    gd_id = models.CharField(max_length=50)
    creation_date = models.DateField()
    creation_time = models.TimeField()


class AreaName(models.Model):
    district = models.CharField(max_length=50)


class PSNames(models.Model):
    psname = models.CharField(max_length=150)


class CrimeNews(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()


class LocalIntelligence(models.Model):
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    date = models.DateTimeField()
    files = models.FileField(upload_to='intelligence_files/')
    psname = models.CharField(max_length=100)
    details = models.TextField()
