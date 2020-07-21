from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, JobApplication
from .models import JobApplication
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from itertools import groupby


# Create your views here.


class PostListView(ListView):
	model = Post
	template_name='Posts/Home.html'
	context_object_name = 'posts'
	ordering = ["-DatePosted"]
	
	paginate_by=3

	def get_queryset(self):
		pos = Post.objects.all()
		data = self.request.GET.get('searchtxt')
		date_min = self.request.GET.get('start_date')
		date_max = self.request.GET.get('end_date')

		if data == '':
			pos = Post.objects.all()
		elif data != '' and data is not None:
			if Post.objects.filter(Location__contains=data):
				pos = Post.objects.filter(Location__contains=data)
				
			elif Post.objects.filter(SkillsRequired__contains=data):
				pos = Post.objects.filter(SkillsRequired__contains=data)

			elif Post.objects.filter(Designation__contains=data):
				pos = Post.objects.filter(Designation__contains=data)

			elif Post.objects.filter(Creator__username__contains=data):
				pos = Post.objects.filter(Creator__username__contains=data)
		
		return pos.order_by('-DatePosted')


class PostDetailView(DetailView):
	model=Post

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		userinfo = self.request.user
		applyjob = self.request.GET.get('applyjob')
		if self.request.method=="GET":
			
			if applyjob:
				postby=Post.objects.get(id=applyjob)
				check = JobApplication.objects.filter(AppliedFor=postby,AppliedBy=userinfo)
				if check.exists():
					messages.warning(self.request,f'You have already applied for this job')
				else:
					apply_job=JobApplication.objects.create(AppliedBy=userinfo,AppliedFor=postby)
					apply_job.save()
					messages.success(self.request,'Job Applied Successfully')
				
		return context


@login_required
def PostJob(request):
	if request.method == "POST":
		Designation = request.POST.get('Designation')
		indtytpe = request.POST.get('indtytpe')
		expfrom = request.POST.get('expfrom')
		expto = request.POST.get('expto')
		jobdisc = request.POST.get('jobdisc')
		Skills = request.POST.get('Skills')
		Qualification = request.POST.get('Qualification')
		emptype = request.POST.get('optradio')
		package = request.POST.get('package')
		Vacancy = request.POST.get('Vacancy')
		location = request.POST.get('location')
		creator = request.user

		experience = expfrom + '-' + expto + ' years'
			
		
		postdetail = Post.objects.create(Designation=Designation, Vacancy=Vacancy, Location= location,Experience=experience, IndustryType=indtytpe, Package=package,
			SkillsRequired=Skills, JobDescription=jobdisc, EmployementType=emptype, Qualification=Qualification, Creator=creator)
		postdetail.save()
		messages.success(request,'Your Job posted successfully')

	return render(request,'Posts/PostJob.html')

def AboutUs(request):
	return render(request,'Posts/AboutUs.html')

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
	model=Post
	success_url='/'

	def test_func(self):
		post=self.get_object()
		if self.request.user == post.Creator:
			return True
		else:
			messages.warning(self.request,'This post you cannot update, Permission Denied, Only post owner can update.')
			return False


class UserPostListView(ListView):
	model=Post
	template_name="Posts/user_posts.html"
	context_object_name = 'posts'
	paginate_by=5

	def get_queryset(self):

		user=get_object_or_404(User, username=self.kwargs.get('username'))
		pos = Post.objects.filter(Creator=user)
		
		return pos


class AppliedJobView(LoginRequiredMixin,ListView):
	model=JobApplication
	template_name='Posts/AppliedJob.html'
	context_object_name='posts'
	paginate_by=5

	def get_queryset(self):

		posts = JobApplication.objects.filter(AppliedBy=self.request.user).order_by('-DateApplied')
		return posts
	
class ReceivedJobView(LoginRequiredMixin,ListView):
	model=JobApplication
	template_name='Posts/ReceivedJob.html'
	context_object_name='posts'
	
	def get_queryset(self):
		
		jobid = Post.objects.filter(Creator=self.request.user)
		posts = JobApplication.objects.filter(AppliedFor__Creator=self.request.user).order_by('AppliedFor')
		
		
		#posts = JobApplication.objects.filter(AppliedFor=jobid).order_by('-DateApplied')
		
		#posts = Post.objects.filter(Creator=self.request.user)
		return posts

class UserJobPostListView(LoginRequiredMixin,ListView):
	model=Post
	template_name="Posts/ReceivedJobList.html"
	context_object_name = 'posts'
	paginate_by=5

	def get_queryset(self):

		#user=get_object_or_404(User, username=self.request.user)
		pos = Post.objects.filter(Creator=self.request.user).order_by('-DatePosted')
		
		return pos