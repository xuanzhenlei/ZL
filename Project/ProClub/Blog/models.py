#from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.conf import settings

# Create your models here.
class blogs(models.Model):
    title = models.CharField(max_length=200)
    cate = models.CharField(max_length=50)
    date=models.DateField(auto_now=True)
    artical = models.TextField()
    img=models.ImageField(upload_to='', blank=True, null=True)
    def __unicode__(self):
        return self.title