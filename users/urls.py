from django.urls import path
import users.views

urlpatterns = [
    path('login/', users.views.login_handler),
    path('logout/', users.views.logout_handler),
    path('switch/', users.views.switch_title),
    path('register/', users.views.register_handler)
]
