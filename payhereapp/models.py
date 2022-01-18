# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db   import models
from core.models import TimeStampModel, SoftDeleteModel

class User(models.Model):
    nickname     = models.CharField(max_length=40, null=True)
    email        = models.EmailField(max_length=200, unique=True)
    password     = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'users'

class Book(TimeStampModel, SoftDeleteModel): 
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    amount      = models.IntegerField(null=True)
    memo        = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = 'books'