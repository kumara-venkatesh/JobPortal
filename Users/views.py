from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
from . models import JSProfile, EmProfile
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm, UserPwdForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_user(request):
	if request.method == 'POST':
		uname = request.POST.get('uname')
		pwd = request.POST.get('pwd')
	
		user = authenticate(username=uname,password=pwd)
		if user is not None:
			login(request, user)
			return redirect('Posts')
		else:
			messages.warning(request,"Username and Password is Invalid")

	return render(request,'Users/Login.html')

def Register(request):
	if request.method == 'POST' and request.FILES['myfile']:
		email = request.POST.get('email')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		cnumber = request.POST.get('cnumber')
		birthday = request.POST.get('birthday')
		address = request.POST.get('address')
		myfile = request.FILES['myfile']
		fs=FileSystemStorage()
		filename=fs.save(myfile.name, myfile)
		password = request.POST.get('password')

		ph = JSProfile.objects.filter(phoneno=cnumber)
		mail = User.objects.filter(email=email)

		if ph.exists():
			messages.warning(request,f'Phone number already exists, please provide your personal phone number')
		elif mail.exists():
			messages.warning(request,f'Email ID already exists, please provide your personal Email address')
		else:
			userdetail = User.objects.create(username=email, first_name=fname, last_name=fname, email=email)
			userdetail.set_password(password)		
			userdetail.save()
			userprofile = JSProfile.objects.create(user=userdetail, BirthDate=birthday, phoneno=cnumber, address=address, Resume=myfile)
			userprofile.save()
			send_mail( 'Registratoin', 'Thank you for registering to Job portal(Trial) Version', settings.EMAIL_HOST_USER, [email], fail_silently=False, )
			messages.success(request,'Account created successfully for "{}" Please login and complete your profile'.format(email))
			return redirect('Login')
			
	return render(request,'Users/Register.html')

def EmpRegister(request):
	if request.method == 'POST':
		email = request.POST.get('oemail')
		cname = request.POST.get('cname')
		address = request.POST.get('address')
		password = request.POST.get('password')
		cperson = request.POST.get('cperson')
		indtytpe = request.POST.get('indtytpe')

		mail = User.objects.filter(email=email)

		if mail.exists():
			messages.warning(request,f'Email ID already exists, please provide your official Email address')
		else:
			empdetail = User.objects.create(username=email, email=email)
			empdetail.set_password(password)
			empdetail.save()
			empprofile = EmProfile.objects.create(user=empdetail, CompanyName=cname, CompAddress= address, IndType=indtytpe, ContactPerson=cperson)
			empprofile.save()
			send_mail( 'Registratoin', 'Thank you for registering to Job portal(Trial) Version', settings.EMAIL_HOST_USER, [email], fail_silently=False, )
			messages.success(request,'Account created successfully for {} please login and complete your profile'.format(email))
			return redirect('Login')

	return render(request,'Users/EmpRegister.html')

@login_required
def Profile(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		cnumber = request.POST.get('cnumber')
		birthday = request.POST.get('birthday')
		address = request.POST.get('address')
		qual = request.POST.get('qual')
		Skills = request.POST.get('Skills')
		optradio = request.POST.get('optradio')
		Designation = request.POST.get('Designation')
		compname = request.POST.get('compname')
		expfrom = request.POST.get('expfrom')
		expto = request.POST.get('expto')

		

		if request.FILES.__contains__('myfile'):
			myfile = request.FILES['myfile']
			fs=FileSystemStorage()
			filename=fs.save(myfile.name, myfile)
			
		else:
			myfile = request.user.jsprofile.Resume
			


		if request.FILES.__contains__('myprofile') :
			myprofile = request.FILES['myprofile']
			fs=FileSystemStorage()
			filename=fs.save(myprofile.name, myprofile)
		else:
			myprofile = request.user.jsprofile.img


		if birthday:
			pass
		else:
			birthday=request.user.jsprofile.BirthDate
		if qual:
			pass
		else:
			qual=request.user.jsprofile.Qualification


		


		ph = JSProfile.objects.filter(phoneno=cnumber)
		mail = User.objects.filter(email=email)

		if ph.exists() and not cnumber==request.user.jsprofile.phoneno:
			messages.warning(request,f'Phone number already exists, please provide your personal phone number')
		elif mail.exists() and not email==request.user.email:
			messages.warning(request,f'Email ID already exists, please provide your personal Email address')
		else:
			jsdetailupdate = request.user
			jsprofileupdate = JSProfile.objects.get(user=request.user)

			if optradio:
				pass
			else:
				experience = request.user.jsprofile.Experience
				jsprofileupdate.CompanyName=request.user.jsprofile.CompanyName
				jsprofileupdate.Designation= request.user.jsprofile.Designation

			if optradio == 'Fresher':
				experience = optradio
				jsprofileupdate.CompanyName=''
				jsprofileupdate.Designation=''

			elif optradio == 'Experienced':
				experience = expfrom + ' ' + expto
				jsprofileupdate.CompanyName=compname
				jsprofileupdate.Designation=Designation

			jsdetailupdate.email= email
			jsdetailupdate.username=email

			if myprofile:
				jsprofileupdate.img=myprofile
			if myfile:
				jsprofileupdate.Resume=myfile

			jsprofileupdate.phoneno=cnumber
			jsprofileupdate.address=address
			jsprofileupdate.BirthDate=birthday
			jsprofileupdate.Qualification=qual
			jsprofileupdate.Skills=Skills
			jsprofileupdate.Experience=experience
			
			

			jsdetailupdate.save()
			jsprofileupdate.save()

			messages.success(request,f'Profile Details updated successfully')
			return redirect('profile')
	

	return render(request,'Users/Profile.html')

@login_required
def password_change(request):
	if request.method == 'POST':
		form=UserPwdForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Your password has successfully updated, please login.')
			return redirect('Login')

	else:
		form=UserPwdForm(request.user)
	
	return render(request,'Users/password_change.html',{'form':form})

@login_required
def EmpProfile(request):
	if request.method == 'POST':
		email = request.POST.get('oemail')
		cname = request.POST.get('cname')
		address = request.POST.get('address')
		cperson = request.POST.get('cperson')
		indtype = request.POST.get('indtype')
		if request.FILES:
			myfile = request.FILES['myfile']
		else:
			myfile = request.user.emprofile.img
		fs=FileSystemStorage()
		filename=fs.save(myfile.name, myfile)
		if indtype:
			pass
		else:
			indtype=request.user.emprofile.IndType

		mail = User.objects.filter(email=email)


		if mail.exists() and not email==request.user.email:
			messages.warning(request,f'Email ID already exists, please provide your official Email address')
			
		else:
			empdetailupdate = request.user
			empdetailupdate.email= email
			empdetailupdate.username=email

			empprofileupdate = EmProfile.objects.get(user=request.user)
			empprofileupdate.CompanyName=cname
			empprofileupdate.CompAddress=address
			empprofileupdate.IndType=indtype
			empprofileupdate.ContactPerson=cperson
			if myfile:
				empprofileupdate.img=myfile
			

			empdetailupdate.save()
			empprofileupdate.save()

			messages.success(request,f'Profile Details updated successfully')
			return redirect('emp_profile')



	return render(request,'Users/EmpProfile.html')
