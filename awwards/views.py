from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse 

# Create your views here.
#  create endpoint for profile_list
@api_view(['GET','POST'])
def profile_list(request):
    if request.method == 'GET':
        profile = Profile.objects.all()
        serialize = ProfileSerializer(profile,many=True)
        return Response(serialize.data)

    elif request.method == 'POST':
        serialize = ProfileSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status.HTTP_201_CREATED)
        return Response(serialize.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def profile_detail(request,id):
    try:
        profile=Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialize = ProfileSerializer(profile)
        return Response(serialize.data)
    
    elif request.method == 'PUT':
        serialize = ProfileSerializer(profile, request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method =='DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT_)

# create endpoint for projects
@api_view(['GET',])
def project_list(request):
    pass


