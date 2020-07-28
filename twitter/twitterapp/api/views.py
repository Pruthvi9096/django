from rest_framework import views
from .serializers import MainSerializer,AttributeSerializer
from ..models import Attribute,Main
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

class mainListCreateView(ListCreateAPIView):
    queryset = Main.objects.all().order_by('id')
    serializer_class = MainSerializer

class attributeListCreateView(ListCreateAPIView):
    queryset = Attribute.objects.all().order_by('id')
    serializer_class = AttributeSerializer

    # def get_serializer_class(self):
    #     self.get
    #     if self.action == 'list':
    #         return AttributeGetSerializer
    #     if self.action == 'post':
    #         return AttributeSerializer

# class mainListCreateView(views.APIView):

#     def get(self,request,format=None):
#         mains = Main.objects.all().order_by('-id')
#         serializer = MainSerializer(mains,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)

#     def post(self,request,format=None):
#         data = request.data
#         serializer = MainSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)

class mainDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Main.objects.all().order_by('id')
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'
    serializer_class = MainSerializer


class attributeDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Attribute.objects.all().order_by('id')
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'
    serializer_class = AttributeSerializer

# class mainDetailUpdateDeleteView(views.APIView):

#     def get(self,request,pk,format=None):
#         main = get_object_or_404(Main,pk=pk)
#         serializer = MainSerializer(main)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     def put(self,request,pk,format=None):
#         main = get_object_or_404(Main,pk=pk)
#         data = request.data
#         serializer = MainSerializer(data=data,instance=main)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self,request,pk,format=None):
#         main = get_object_or_404(Main,pk=pk)
#         main.delete()
#         return Response({"message":"Deleted !"},status=status.HTTP_204_NO_CONTENT)

