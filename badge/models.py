from django.db import models

# Create your models here.
class Badge(models.Model):
    badge_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    content = models.TextField()