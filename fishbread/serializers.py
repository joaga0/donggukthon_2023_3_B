from rest_framework import serializers
from .models import *

class FishbreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fishbread
        fields = '__all__'