from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User
from fishbread.models import Fishbread
# from .serializers import UserSerializer
from fishbread.serializers import FishbreadSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET', 'POST'])
def fishbread_info(request):

    if request.method == 'GET':
        fishbreads = Fishbread.objects.all()
        serializer = FishbreadSerializer(fishbreads, many=True)
        return Response(data=serializer.data)
    
    if request.method == 'POST':
        serializer = FishbreadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)

@api_view(['GET', 'POST'])
def fishbread_detail(request, id):
    user = get_object_or_404(User, user_id=id)

    if request.method == 'GET':
        fishbreads = Fishbread.objects.filter(user_id=user)
        serializer = FishbreadSerializer(fishbreads, many=True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        serializer = FishbreadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)