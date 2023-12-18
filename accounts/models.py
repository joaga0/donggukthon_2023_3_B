from django.db import models
# from fishbread.models import Fishbread

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=20)
    account = models.IntegerField()
    day = models.IntegerField(default=0)    #몇일차인지
    sum = models.IntegerField(default=0)    #현재총모인금액
    # fishbread = models.ForeignKey(Fishbread, blank=False, null=False, on_delete=models.CASCADE)  #랜덤 붕어빵
    # donation = models.IntegerField(default=0)

    # class Random_Fish(models.IntegerChoices):
    #     fish1 = 1
    #     fish2 = 2
    # fishbread = []
    # fishbread = models.IntegerField(choices=Random_Fish.choices)