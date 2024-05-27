from django.urls import path

import users.views

urlpatterns = [path("switch", users.views.UsersViews.as_view(), name="users")]
