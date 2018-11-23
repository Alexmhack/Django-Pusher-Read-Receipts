from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from message.views import (broadcast, conversations, delivered)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += [
    path('conversation/', broadcast, name='broadcast'),
    path('conversations/', conversations, name='conversations'),
    path('conversations/<int:id>/delivered/', delivered, name='delivered'),
]
