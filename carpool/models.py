import uuid
from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True,max_length=200)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class EmailConfirmation(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4())

    
class Trip(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)
    date = models.DateTimeField()
    seats_available = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.start_location} {self.end_location} {self.date}"


class CompanionRequest(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return f"{self.start_location} {self.end_location} {self.date}"