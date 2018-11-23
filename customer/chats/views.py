from django.shortcuts import render
from django.http import JsonResponse

from pusher import Pusher
from decouple import config

pusher = Pusher(
	app_id='2',
	key=config('PUSHER_KEY'),
	secret=config('PUSHER_SECRET'),
	cluster=config('PUSHER_CLUSTER'),
	ssl=True
)


def index_view(request):
	return render(request, 'index.html')


def chat_admin_view(request):
	return render(request, 'chat_admin.html')
