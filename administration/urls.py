from django.urls import path
from . import views
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path, include
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('order/new/', views.neworder, name='neworder'),
    path('order/list/', views.listorder, name='listorder'),
    path('order/pending/', views.pendingorders, name='pendingorders'),
    path('order/edit/<int:pk>', views.editorder, name='editorder'),
    path('order/delete/<int:pk>', views.deleteorder, name='deleteorder'),
    path('order/active/<int:pk>', views.activeorder, name='activeorder'),
    path('service/add/<int:pk>', views.addservice, name='addservice'),
    path('service/new/<int:pk>', views.newservice, name='newservice'),
    path('service/list/', views.listservice, name='listservice'),
    path('services/list/', views.listservices, name='listservices'),
    path('services/edit/<int:pk>', views.editservices, name='editservices'),
    path('service/edit/<int:pk>', views.editservice, name='editservice'),
    ]