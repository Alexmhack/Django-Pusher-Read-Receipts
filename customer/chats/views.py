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
	return render(request, 'chats/index.html')


def chat_admin_view(request):
	return render(request, 'chat_admin.html')


def guest_user(request):
	name = request.POST.get('name', '')
	email = request.POST.get('email', '')

	pusher.trigger('general-channel', 'new-guest-details', {
		'name': name,
		'email': email
	})

	return JsonResponse({'name': name, 'email': email})


def pusher_authentication(request):
	channel_name = request.POST.get('channel_name')
	socket_id = request.POST.get('socket_id')

	auth = pusher.authenticate(channel=channel_name, socket_id=socket_id)

	return JsonResponse({'channel_name': channel_name, 'socket_id': socket_id})
