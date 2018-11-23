from django.urls import path

from .views import index_view, chat_admin_view, guest_user, pusher_authentication

urlpatterns = [
	path('', index_view, name='index'),
	path('chat/admin/', chat_admin_view, name='chat_admin'),
	path('new/guest/', guest_user, name='new_guest'),
	path('pusher/auth/', pusher_authentication, name='pusher_auth'),
]
