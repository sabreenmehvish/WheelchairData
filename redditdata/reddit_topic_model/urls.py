from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_model', views.generate_model, name='generate_model')
]