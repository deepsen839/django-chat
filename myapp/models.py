from django.db import models

# Create your models here.
class Status(models.Model):
    status = models.BooleanField(default=1)