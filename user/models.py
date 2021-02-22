from django.db import models

# Create your models here.
class User(models.Model):

    name = models.CharField(max_length=50, blank=True)
    alias = models.CharField(max_length=80, blank=False, default='NOT_SET')
    email = models.EmailField(blank=True)
    mturk_id = models.CharField(max_length=100, blank=False, default='NOT_SET')
    attendance_id = models.CharField(max_length=50, blank=True, null=True)
    uuid = models.CharField(max_length=100, blank=True, null=True)

    def setUuid(self):
        newUuid = str(abs(hash(str(self.name) + str(self.alias) + str(self.email) + str(self.mturk_id) + str(self.attendance_id)))%100000000)
        self.uuid = newUuid
        print('changed success!', str(self.uuid))
        self.save()

    def __str__(self):
        return  "User{ " + 'id: ' + str(self.id) + ', name: ' + str(self.name) + ', alias: ' + str(self.alias) + ', email: ' + str(self.email) + ', mturk id: ' + str(self.mturk_id) + ", uuid: " + str(self.uuid)[:10] + " }"
