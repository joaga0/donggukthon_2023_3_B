from django.db import models

# Create your models here.
class Badge(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    image = models.ImageField(blank=False, null=False)

    def __str__(self) -> str:
        return self.name
