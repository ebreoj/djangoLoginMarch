from __future__ import unicode_literals

from django.db import models

import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class userManager(models.Manager):
	def regValidator(self, postData):
		errors = {}
		if User.objects.filter(email = postData['email']):
		 	errors['email_exists'] = "You have an existing account yo!."
		if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
			errors['first_name'] = "3? you can do more than that!, numerical is not allowed."
		if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
			errors['last_name'] = "I explained this to you already! I said 3 or more!, numerical is not allowed."
		if EMAIL_REGEX.match(postData['email']) == None:
			errors['email_format'] = "Email must be valid."
		if len(postData['password']) < 8:
			errors['pword_length'] = "Password must be at least 8 characters long."
		if postData['password'] != postData['pwconf']:
			errors['pwconf'] = "Password confirmation must match password."
		print errors
		return errors
	def loginValidator(self, postData):
		user = User.objects.filter(email = postData['login_email'])
		print user
		errors = {}
		if not user:
			errors['email'] = "valid email address please!."
		if user:
			password = User.objects.get(email = postData['login_email']).password
			if bcrypt.checkpw(postData['login_password'].encode(), password.encode()) != True:
				errors['password'] = "Invalid password."
		# if user and not bcrypt.checkpw(postData['login_password'].encode('utf8'), user[0].password.encode('utf8')):
		# 	errors['password'] = "Invalid password."
		return errors

# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	def __repr__(self):
		return '<user object {} {} {} {}>'.format(self.first_name, self.last_name, self.email, self.password)

	objects = userManager()

