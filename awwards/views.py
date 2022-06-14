from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect 
from django.urls import reverse
from django.db.models import Q

import requests

from .forms import NewUserForm, ProjectForm, ReviewForm, UpdateUserProfileForm, UpdateUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("login")

# User Profile
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    if request.user == user_profile:
        return redirect('profile', username=request.user.username)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'edit_profile.html', context)


def index(request):
    form = ReviewForm()
    projects = requests.get('http://127.0.0.1:8000/project/').json()
    return render(request, "index.html", {"projects": projects, "form": form})

def project_details(request, project_id):
    # This restricts only logged in users to access this page
    print(project_id)
    if not request.user.is_authenticated:
        messages.info(request, "You must be logged in to access this page.") 
        return HttpResponseRedirect(reverse('login'))
    results = Project.objects.filter(id=project_id).get()
    print(results.image)
    context = {'results': results}
    return render(request, "project.html", context)


# Adding a new project
def new_project(request):
    if not request.user.is_authenticated:
        messages.info(request, "You must be logged in to access this page.") 
        return HttpResponseRedirect(reverse('login'))
    form =ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('add_project')

    return render(request, 'add_project.html', {'form': form})


# Search for projects
def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            projects = Project.objects.filter(title__icontains=query)
            return render(request, 'search.html',{"projects": projects})

        else:
            message = "You haven't searched for any image"
            return render(request, 'search.html',{"message":message})

# Project Rating
def review(request,project_id ):
    user = request.user
    project=Project.objects.get(id=project_id)
    if request.method == 'POST':
        form=ReviewForm(request.POST )
        if form.is_valid():
            form=form.save(commit=False)
            form.project=project
            form.save()
            design = request.POST['design']
            usability = request.POST['usability']
            content = request.POST['content']
            rates=(int(design)+int(usability)+int(content))/3

        return render(request, 'project.html', {'rates':rates,'project':project})
    else:
        form=ReviewForm()
    return render(request, 'project.html', {'user':user,'form':form,'project':project})





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
    if request.method == 'GET':
        project = Project.objects.all()
        serialize = ProjectSerializer(project,many=True)
        return Response(serialize.data)

    elif request.method == 'POST':
        serialize = ProjectSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status.HTTP_201_CREATED)
        return Response(serialize.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def project_detail(request,id):
    try:
        project=Project.objects.get(id=id)
    except Project.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialize = ProjectSerializer(project)
        return Response(serialize.data)
    
    elif request.method == 'PUT':
        serialize = ProjectSerializer(project, request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method =='DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT_)
