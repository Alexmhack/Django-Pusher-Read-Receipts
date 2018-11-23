from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from pusher import Pusher
from .models import Conversation

# instantiate pusher
pusher = Pusher(
	app_id='b3687ab4-115b-40a1-aeaf-431e117cbb35',
	key='b3687ab4-115b-40a1-aeaf-431e117cbb35',
	secret='cBBp5PhCPL82Ff4mEuGYxwb0jaTdnSaZf/O7dK0gTgI=',
	cluster='v1:us1:b3687ab4-115b-40a1-aeaf-431e117cbb35')

@login_required()
def index(request):
	return render(request, 'chat.html')


@csrf_exempt
def broadcast(request):
	con_msg = request.POST.get('message', '')
	message = Conversation(message=con_msg, status='', user=request.user)
	message.save()

	pusher_msg = {
		'name': message.user.username,
		'status': message.status,
		'message': message.message,
		'id': message.id,
		'created_at': message.created_at
	}

	# trigger the message channel and event to pusher
	pusher.trigger('a_channel', 'an_event', pusher_msg)

	# return json response of the broadcasted message
	return JsonResponse(pusher_msg)

def conversations(request):
	data = Conversation.objects.all()
	con_data = [{
		'name': message.user.username,
		'status': message.status,
		'message': message.message,
		'id': message.id,
		'created_at': message.created_at
	} for message in data]

	# return json response of broadcasted messages
	return JsonResponse(con_data)


@csrf_exempt
def delivered(request, id):
	message = Conversation.objects.get(id=id)

	if request.user.id != message.user.id:
		socket_id = request.POST.get('socket_id', '')
		message.status = 'Delivered'
		message.save()

		push_msg = {
			'name': message.user.username,
			'status': message.status,
			'message': message.message,
			'id': message.id,
			'created_at': message.created_at
		}
		pusher.trigger('a_channel', 'delivered_message', message, socket_id)
		return HttpResponse('OK')
	else:
		return HttpResponse('Awaiting Delivery')
