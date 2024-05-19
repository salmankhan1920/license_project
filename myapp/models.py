from django.db import models

# Create your models here.
# license_manager/models.py

# class LicenseKey(models.Model):
#     key = models.CharField(max_length=20, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.key


class LicenseKey(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
