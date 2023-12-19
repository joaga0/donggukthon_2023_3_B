from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Badge
from .serializers import BadgeSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET'])
def badge_list(request):
    if request.method == 'GET':
        badges = Badge.objects.all()
        serializer = BadgeSerializer(badges, many=True)
        return Response(data=serializer.data)
        
@api_view(['GET'])
def acquired_badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)

    if request.method == 'GET':
        serializer = BadgeSerializer(badge)
        return Response(serializer.data)
    
    # elif request.method == 'PATCH':
    #     serializer = BadgeSerializer(instance=badge, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response(data=serializer.data)
    
    # elif request.method == 'DELETE':
    #     badge.delete()
    #     data = {
    #         'delete_fishbread':id
    #     }
    #     return Response(data)