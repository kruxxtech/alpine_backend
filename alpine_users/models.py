from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.


class User(AbstractUser):
    ROLES = (("admin", "admin"), ("staff", "staff"))
    role = models.CharField(max_length=10, choices=ROLES)
