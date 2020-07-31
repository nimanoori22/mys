from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    postal_code = models.IntegerField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

