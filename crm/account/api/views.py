from rest_framework.decorators import api_view
from account.models import Customer
from .serializers import CustomerSerializer
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import render,get_object_or_404

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
        return JsonResponse({'message':'Customer was deleted successfully'},status=status.HTTP_204_NO_CONTENT)


def game(request):
    return render(request,'fourdots.html',{})