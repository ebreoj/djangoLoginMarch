from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from models import *
import bcrypt

# Create your views here.
def index(request):
	return render(request,'first_app/index.html')

def register(request):
	msgs = User.objects.regValidator(request.POST)
	if len(msgs):
		for a,b in msgs.iteritems():
			print a,b
		 	messages.error(request, b, extra_tags=a)
	else:
		hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email=request.POST['email'], password=hashedpw)
		user = User.objects.last()
		request.session['logged_in'] = user.id
		print request.session['logged_in']
		return redirect('/success')

	return redirect('/')

def login(request):
	print 'logging in'
	errors = User.objects.loginValidator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	
	user = User.objects.get(email=request.POST['login_email'])
	request.session['logged_in'] = user.id
		
	return redirect('/success')

def success(request):
	if User.objects.get(id=request.session['logged_in']) == User.objects.last():
		status = "registered"
	else:
		status = "logged in"

	context = {'user': User.objects.get(id=request.session['logged_in']), 'status': status}
	return render(request, 'first_app/success.html', context)