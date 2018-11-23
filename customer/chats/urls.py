from django.urls import path

from .views import index_view, chat_admin_view

urlpatterns = [
	path('', index_view, name='index'),
	path('chat_admin/', chat_admin_view, name='chat_admin'),
]
