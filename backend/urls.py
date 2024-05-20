from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/universities', include('universities.urls')),
    path('api/v1/specialities', include('specialities.urls')),
    path('api/v1/registry/', include('registry.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
    path('api/v1/auth/users/manage/', include('users.urls'))
]
