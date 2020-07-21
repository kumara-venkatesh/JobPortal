from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator,MinLengthValidator, int_list_validator
from django.utils import timezone
from PIL import Image

# Create your models here.
class JSProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
	img = models.ImageField(default='default.jpg', upload_to='profile_pics/')
	BirthDate = models.DateField()
	phoneno = models.CharField(max_length=10, validators=[int_list_validator(sep=''),MinLengthValidator(10),RegexValidator(r'^\d{0,10}$')])
	address = models.CharField(max_length=200)
	Qualification = models.CharField(max_length=200, blank=True)
	Resume = models.FileField(upload_to='Files/')
	Designation = models.CharField(max_length=100, blank=True)
	Experience = models.CharField(max_length=100,blank=True)
	CompanyName = models.CharField(max_length=100, blank=True)
	Skills = models.CharField(max_length=500, blank=True)
	

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self,**kwargs):
		super().save()

		image=Image.open(self.img.path)

		if image.width >300 and image.height > 300:
			output_size=(300,300)
			image.thumbnail(output_size)
			image.save(self.img.path)

class EmProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
	img = models.ImageField(default='default.jpg', upload_to='profile_pics/')
	CompanyName = models.CharField(max_length=100)
	CompAddress = models.CharField(max_length=200)
	IndType = models.CharField(max_length=100)
	ContactPerson = models.CharField(max_length=100)
	

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self,**kwargs):
		super().save()

		image=Image.open(self.img.path)

		if image.width >300 and image.height > 300:
			output_size=(300,300)
			image.thumbnail(output_size)
			image.save(self.img.path)