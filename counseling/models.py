from django.db import models

class Counselor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
