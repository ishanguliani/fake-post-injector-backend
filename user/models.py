from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    attendance_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name