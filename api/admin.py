from django.contrib import admin

# Register your models here.
from .models import Img

class ImgAdmin(admin.ModelAdmin):
	class Meta:
		model = Img
		fields = ['image', 'timestamp']

admin.site.register(Img, ImgAdmin)
