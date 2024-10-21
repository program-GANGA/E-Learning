from django.db import models
from django.contrib.auth.models import User



class Admin_Model(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    username=models.CharField(max_length=220,unique=True)
    password=models.CharField(max_length=220)

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skype_id = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, default='default@example.com')
    phone = models.CharField(max_length=10,default='0000000000')
    courses = models.ManyToManyField('student.Course', related_name='trainers')

# Create your models here.
