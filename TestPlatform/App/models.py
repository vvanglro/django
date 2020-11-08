from django.db import models

# Create your models here.

class Module(models.Model):

    m_name = models.CharField(max_length=24, unique=True)


class Case(models.Model):

    c_name = models.CharField(max_length=24)
    c_method = models.CharField(max_length=10)
    c_url = models.CharField(max_length=256)
    c_header = models.CharField(max_length=1000, null=True, blank=True)
    c_data = models.CharField(max_length=1000, null=True, blank=True)
    c_code = models.CharField(max_length=24)
    c_result = models.CharField(max_length=100)
    c_module = models.ForeignKey(Module)