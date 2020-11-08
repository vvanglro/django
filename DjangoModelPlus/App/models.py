from django.db import models


# django_migrations表中会记录迁移记录



class Student(models.Model):
    s_name = models.CharField(max_length=16)
    s_age = models.IntegerField(default=1)


class Grade(models.Model):
    g_name = models.CharField(max_length=16)
