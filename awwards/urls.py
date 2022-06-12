from django.urls import path
from .views import *
from . import views


urlpatterns=[
    path('', views.index, name='index'),
    path('project_details/<int:project_id>', views.project_details, name='project-details'),
    path('profile/',profile_list),
    path('profile/<int:id>',profile_detail),
    path('project/',project_list),
    path('project/<int:id>',project_detail),
    path('register/', views.register_request, name='register'),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("add_project/", views.new_project, name= "add_project"),

]