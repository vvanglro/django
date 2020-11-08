from django.db import models

# Create your models here.
class Student(models.Model):
    s_name = models.CharField(max_length=16)

    def get_name(self):
        return self.s_name