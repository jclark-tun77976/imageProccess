from django.db import models

class Image(models.Model):
    original = models.ImageField(upload_to='uploads/')
    filtered = models.ImageField(upload_to='processed/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original.name