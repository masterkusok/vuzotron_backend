from django.urls import path
import universities.views

urlpatterns = [
    path('', universities.views.UniversityView.as_view(), name='universities')
]
