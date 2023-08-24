from django.db import models
import os
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.

class ManagedFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='upload/')

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=ManagedFile)
def delete_file(sender, instance, **kwargs):
    # Get the path of the file on disk
    print("entring in delete fucntion")
    if instance.file:
        file_path = os.path.join(settings.MEDIA_ROOT, str(instance.file))
        # Delete the file from disk
        print("file_path __________will be ", file_path)
        if os.path.exists(file_path):
            os.remove(file_path)