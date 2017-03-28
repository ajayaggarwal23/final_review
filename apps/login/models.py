from django.db import models
import re
from datetime import date, datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def create_user(self, data):
        errors = []
        try:
            user_check = Userentry.objects.get(email=data['email'])
            print user_check
            if user_check.email == data['email']:
                errors.append("Email Already Registered -- Please Try to Login")
        except:
            pass
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Not a valid email address")
        if any(i.isdigit() for i in data['name']):
            errors.append("No numbers in Name")
        if len(data['name']) < 2:
            errors.append("First Name Must Be 2 or more characters")
        if not data['birthday']:
            errors.append("Please enter a valid birthday")
        if len(data['passwd']) < 8:
            errors.append("Password Must Be atleast 8 characters")
        if len(data['passwdconf']) < 8:
            errors.append("Password Confirmation Must Be atleast 8 characters")
        if data['passwd'] != data['passwdconf']:
            errors.append("Passwords Must Match")
        if errors:
            return (False, errors)
        else:
            hashed = bcrypt.hashpw(data['passwd'].encode(), bcrypt.gensalt())
            new_entry = Userentry.objects.create(email=data['email'], name=data['name'], birthday=data['birthday'], passwd=hashed)
            return (True, new_entry)

    def check_user(self, data):
        errors = []
        try:
            returned = Userentry.objects.get(email=data['email'])
            if bcrypt.checkpw(data['passwd'].encode(), returned.passwd.encode()):
                return (True, returned)
            else:
                errors.append("Passwords Incorrect")
                return (False, errors)
        except:
            errors.append("Not a valid email address or password")
            return (False, errors)


class Userentry(models.Model):
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    birthday = models.DateField(auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
