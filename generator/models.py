from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Passw(models.Model):
    title = models.CharField(max_length=300)
    passw = models.CharField(max_length=13)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title