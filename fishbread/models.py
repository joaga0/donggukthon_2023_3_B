from django.db import models
from accounts.models import User

# Create your models here.
class Fishbread(models.Model):
    fishbread_id = models.IntegerField()
    user_id = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    foundation_id = models.IntegerField()
    name = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    day = models.IntegerField(default=0)