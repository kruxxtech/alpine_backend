from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.


class User(AbstractUser):
    ROLES = (("admin", "admin"), ("staff", "staff"))
    role = models.CharField(max_length=10, choices=ROLES)
    first_name = models.CharField(max_length=30, blank=True, null=True, default=None)
    last_name = models.CharField(max_length=30, blank=True, null=True, default=None)
