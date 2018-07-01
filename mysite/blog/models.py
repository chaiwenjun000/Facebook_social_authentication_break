from django.db import models

# Create your models here.

class BlogsPost(models.Model):
	title = models.CharField(max_length = 150)
	body = models.TextField()
	timestamp = models.DateTimeField()
	img = models.ImageField(upload_to='img2')
	
class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=20)

class ImgEncoding(models.Model):
	name = models.TextField() # 名称
	face_recognition_encoding = models.TextField()
