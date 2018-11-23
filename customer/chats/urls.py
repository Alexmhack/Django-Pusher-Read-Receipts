from django.urls import path

from .views import index_view, chat_admin_view, guest_user

urlpatterns = [
	path('', index_view, name='index'),
	path('chat_admin/', chat_admin_view, name='chat_admin'),
	path('new_guest/', guest_user, name='new_guest'),
]
