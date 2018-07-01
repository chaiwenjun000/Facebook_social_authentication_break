from django.contrib import admin
from blog.models import BlogsPost
from blog.models import IMG
from blog.models import ImgEncoding

# Register your models here.
class BlogsPostAdmin(admin.ModelAdmin):
	list_display = ['title','body','timestamp','img']
class IMGAdmin(admin.ModelAdmin):
	list_display = ['img','name']
class ImgEncodingAdmin(admin.ModelAdmin):
	list_display = ['name','face_recognition_encoding']


admin.site.register(BlogsPost,BlogsPostAdmin)
admin.site.register(IMG,IMGAdmin)
admin.site.register(ImgEncoding,ImgEncodingAdmin)