from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/universities', include('universities.urls')),
    path('api/v1/specialities', include('specialities.urls')),
    path('api/v1/registry/', include('registry.urls')),
    path('api/v1/users/', include('users.urls')),
]
