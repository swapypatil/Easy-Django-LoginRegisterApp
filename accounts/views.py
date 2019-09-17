from django.shortcuts import render,redirect
from django.core.mail import send_mail, BadHeaderError
from django.core.mail.backends import smtp
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.




def contact(request):
	if request.method == 'POST':
		email1 = request.POST['email1']
		message1 = request.POST['message1']
		subject = request.POST['subject']
		try:
			send_mail(subject, message1, email1, ['adipandit8891@gmail.com'],)
		except BadHeaderError:
			return HttpResponse('Invalid header found.')
		return redirect('/')
	else:	
		return render(request,'contact.html')
	
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user = auth.authenticate(username=username,password=password)
		
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else:
			messages.info(request,'invalid credentials')
			return redirect('login')
	else:
		return render(request,'login.html')
		
	
def register(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']
		if pass1 == pass2:
			if User.objects.filter(username=username).exists():
				messages.error(request,'username already taken!!!!!!!!!!')
				return redirect('register')
			elif User.objects.filter(email=email).exists():
				messages.info(request,'email already taken!!!!!')
				return redirect('register')
			elif len(pass1) < 8:
				messages.info(request,"password must be 8 character in length")
			else:
				user = User.objects.create_user(username = username,password = pass1,email = email,first_name = first_name,last_name = last_name )
				user.save();
				messages.info(request,'user created')
				return redirect('login')
			
		else:
			messages.info(request,'password not matching!!!!!!')
			return redirect('register')
		return redirect('/')
	else:
		return render(request,'register.html')
		
		
		
def logout(request):
	auth.logout(request)
	return redirect('/')