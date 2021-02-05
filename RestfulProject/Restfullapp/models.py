from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
