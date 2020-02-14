from django.db import models

# Create your models here.
class User(models.Model):

    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    attendance_id = models.CharField(max_length=50, blank=True, null=True)
    uuid = models.CharField(max_length=100, blank=True, null=True)

    def setUuid(self):
        newUuid = str(abs(hash(str(self.name) + str(self.email) + str(self.attendance_id)))%100000000)
        self.uuid = newUuid
        print('changed success!', str(self.uuid))

    def __str__(self):
        return  "User{ " + 'id: ' + str(self.id) + ', name: ' + str(self.name) + ', email: ' + str(self.email) + ", uuid: " + str(self.uuid)[:10] + " }"
