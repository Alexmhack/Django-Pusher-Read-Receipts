from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.CharField(blank=True, null=True, max_length=256)
	status = models.CharField(blank=True, null=True, max_length=256)
	created_at = models.DateTimeField(auto_now=True)
