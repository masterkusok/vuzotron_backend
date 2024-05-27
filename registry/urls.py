from django.urls import path
from . import views

urlpatterns = [
    path('pull', views.RegistryView.as_view(), name='pull')
]
