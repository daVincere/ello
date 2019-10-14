import os
from django.db import models
from django.conf import settings
from datetime import datetime

def path_and_rename(instance, filename):
	"""
		This function names the file being uploaded and makes it a JPG
	"""
	upload_to = 'test' # Upload Location

	_datetime = datetime.now()
	datetime_str = _datetime.strftime("%m-%d-%H-%M-%S")
	filename = '{}.jpg'.format(datetime_str)
	
	return os.path.join(upload_to, filename)

# Create your models here.
class Img(models.Model):
	image = models.FileField(null=False, blank=False, upload_to=path_and_rename)
	timestamp = models.DateTimeField(auto_now_add=True)