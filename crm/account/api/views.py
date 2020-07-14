from rest_framework.decorators import api_view,renderer_classes
from account.models import Customer,Product
from .serializers import CustomerSerializer,ProductSerializer
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import render,get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import CoreAPIJSONOpenAPIRenderer

class productListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['GET','POST'])
@renderer_classes([CoreAPIJSONOpenAPIRenderer])
def productView(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('id')
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def customerView(request):
    customers = Customer.objects.all().order_by('id')
    serializer = CustomerSerializer(customers,many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
def customerCreateView(request):
    if request.method == 'GET':
        customers = Customer.objects.all().order_by('id')
        serializer = CustomerSerializer(customers,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def getUpdateDeleteCustomer(request,pk):
    customer = Customer.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = CustomerSerializer(customer,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = CustomerSerializer(instance=customer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def game(request):
    return render(request,'fourdots.html',{})