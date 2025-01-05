
# Create your models here.
from django.db import models
class Dht11(models.Model):
  temp = models.FloatField(null=True)
  hum = models.FloatField(null=True)
  dt = models.DateTimeField(auto_now_add=True,null=True)
# models.py
from django.db import models

class Incident(models.Model):
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incident at {self.timestamp} with temperature {self.temperature}"