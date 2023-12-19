from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Fishbread
from .serializers import FishbreadSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
# @api_view(['GET', 'POST'])
# def fishbread_info(request):

#     if request.method == 'GET':
#         fishbreads = Fishbread.objects.all()
#         serializer = FishbreadSerializer(fishbreads, many=True)
#         return Response(data=serializer.data)
    
#     if request.method == 'POST':
#         serializer = FishbreadSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(data=serializer.data)
        
# @api_view(['GET', 'PATCH', 'DELETE'])
# def fishbread_detail(request, id):
#     fishbread = get_object_or_404(Fishbread, user_id=id)

#     if request.method == 'GET':
#         serializer = FishbreadSerializer(fishbread)
#         return Response(serializer.data)
    
#     elif request.method == 'PATCH':
#         serializer = FishbreadSerializer(instance=fishbread, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(data=serializer.data)
    
#     elif request.method == 'DELETE':
#         fishbread.delete()
#         data = {
#             'delete_fishbread':id
#         }
#         return Response(data)