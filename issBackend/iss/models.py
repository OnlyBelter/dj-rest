from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User',
                              related_name='images',
                              on_delete=models.CASCADE)
    userId = models.CharField(max_length=100, blank=False, default='')
    des = models.TextField(blank=True)
    fileUrl = models.CharField(max_length=300, blank=False, default='')
    localImage = models.FileField(upload_to='%Y/%m%d', null=True, blank=True)

    class Meta:
        ordering = ('created',)
