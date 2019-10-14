from rest_framework import serializers 
from .models import Img

class ImgSerializer(serializers.ModelSerializer):
	class Meta:
		model = Img
		fields = ['image']