from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Foundation
from .serializers import FoundationSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET'])
def foundation_list(request):
    if request.method == 'GET':
        foundations = Foundation.objects.all()
        serializer = FoundationSerializer(foundations, many=True)
        return Response(data=serializer.data)
        
@api_view(['GET'])
def foundation_detail(request, id):
    foundation = get_object_or_404(Foundation, foundation_id=id)

    if request.method == 'GET':
        serializer = FoundationSerializer(foundation)
        return Response(serializer.data)
    
    # elif request.method == 'PATCH':
    #     serializer = FoundationSerializer(instance=foundation, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response(data=serializer.data)
    
    # elif request.method == 'DELETE':
    #     foundation.delete()
    #     data = {
    #         'delete_fishbread':id
    #     }
    #     return Response(data)