from rest_framework import serializers
from .models import User

class UserBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields=['holder','bankname','account_num']

class UserDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['date']

# 마이 페이지
class UserSeriazlier(serializers.ModelSerializer):

    class Meta:
        model = User
        fields= ['email', 'name','holder','bankname','account_num', 'date']

# 유저가 가진 붕어빵 
class UserFishbreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['fishbread']