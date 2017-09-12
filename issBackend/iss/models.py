from __future__ import unicode_literals

from django.db import models

# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User',
                              related_name='images',
                              on_delete=models.CASCADE)
    userId = models.CharField(max_length=100, blank=False, default='')
    des = models.TextField(blank=True)
    fileUrl = models.CharField(max_length=300, blank=False, default='')
    localImage = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.owner.username
