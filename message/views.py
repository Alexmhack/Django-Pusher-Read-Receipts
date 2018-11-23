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
