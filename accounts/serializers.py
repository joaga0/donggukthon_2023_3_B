from rest_framework import serializers
from .models import UserManager, User
from django.contrib.auth import get_user_model

class UserBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserManager
        fields=['holder','bankname','account_num']

class UserDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserManager
        fields = ['date']
    
    def update(self, instance, validated_data):
        date = validated_data.get('date', instance.date)

        instance.date = ','.join(map(str, date))
        # instance.date = ','.join(date_list)
        instance.save()

        return instance

# 마이 페이지
class UserSeriazlier(serializers.ModelSerializer):

    class Meta:
        model = UserManager
        fields= ['email', 'name','holder','bankname','account_num', 'date']

# 유저가 가진 붕어빵 
class UserFishbreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserManager
        fields = ['fishbread']




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user