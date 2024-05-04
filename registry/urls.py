from django.urls import path
from . import views

urlpatterns = [
    path('pull', views.pull_data_from_registry, name='pull')
]
