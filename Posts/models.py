from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):

	Designation = models.CharField(max_length=50)
	Vacancy = models.IntegerField()
	Location = models.CharField(max_length=100)
	Experience = models.CharField(max_length=40)
	IndustryType = models.CharField(max_length=50)
	Package = models.CharField(max_length=50)
	SkillsRequired = models.CharField(max_length=150)
	JobDescription = models.TextField()
	EmployementType = models.CharField(max_length=50)
	Qualification = models.CharField(max_length=100)
	DatePosted = models.DateTimeField(default=timezone.now)
	Creator = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.Designation
	
	#def get_absolute_url(self):
		#return reverse('post-detail', kwargs={'pk': self.pk})
class JobApplication(models.Model):
	DateApplied = models.DateTimeField(default=timezone.now)
	AppliedBy = models.ForeignKey(User, on_delete=models.CASCADE)
	AppliedFor = models.ForeignKey(Post,on_delete=models.CASCADE)

	
