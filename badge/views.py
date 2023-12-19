from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Badge
from .serializers import BadgeSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET', 'POST'])
def badge_list(request):
    if request.method == 'GET':
        badges = Badge.objects.all()
        serializer = BadgeSerializer(badges, many=True)
        return Response(data=serializer.data)
    
    if request.method == 'POST':
        serializer = BadgeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        
@api_view(['GET', 'PATCH', 'DELETE'])
def acquired_badge(request, id):
    badge = get_object_or_404(Badge, badge_id=id)

    if request.method == 'GET':
        serializer = BadgeSerializer(badge)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = BadgeSerializer(instance=badge, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data)
    
    elif request.method == 'DELETE':
        badge.delete()
        data = {
            'delete_fishbread':id
        }
        return Response(data)