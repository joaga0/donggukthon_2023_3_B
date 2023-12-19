from rest_framework import serializers
from .models import *

class FoundationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foundation
        fields = '__all__'