from django.urls import path

from . import views

urlpatterns = [
    path("", views.SpecialitiesView.as_view(), name="speciality"),
]
