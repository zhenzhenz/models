from django.db import models

# Create your models here.
class article(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField(null=True)
