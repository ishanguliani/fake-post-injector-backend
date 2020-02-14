from django.db import models

# Create your models here.
class User(models.Model):

    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    attendance_id = models.CharField(max_length=50, blank=True, null=True)
    uuid = models.CharField(max_length=100, blank=False, null=False, default="")

    def __init__(self):
        self.uuid = self.getHash()

    def __hash__(self):
        return self.getHash()

    def getHash(self):
        return hash(str(self.name) + str(self.email) + str(self.attendance_id))

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.name == other.name and self.email == other.email and self.attendance_id == other.attendance_id

    def __str__(self):
        return  "User{ " + 'id: ' + str(self.id) + ', name: ' + str(self.name) + ', email: ' + str(self.email) + " }"