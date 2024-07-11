from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True, blank=True, null=True) 
    grant_token = models.CharField(_('grant token'), max_length=255, unique=True)
    location = models.CharField(_('location'), max_length=5, null=True)
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = None
        super().save(*args, **kwargs)
    
       