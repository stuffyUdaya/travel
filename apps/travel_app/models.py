from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re
import bcrypt

# Create your models here.
# email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex  = re.compile(r'^[a-zA-Z]*$')

class UserManager(models.Manager):
    def userValidator(self,name,u_name,password,confpassword):
        errors = []
        flag= False

        if len(name)<2:
            errors.append(" Name should contain atleast two characters")
            flag = True
        if not name_regex.match(name):
            errors.append(" Name was invalid")
            flag = True
        if len(u_name)<2:
            errors.append("User Name should contain atleast two characters")
            flag = True

        if password!=confpassword:
            errors.append("Passwords must match")
            flag = True
        if len(password)<5:
            errors.append("Password should contain atleast five characters")
            flag = True
        if not flag:
            pwhash = bcrypt.hashpw(str(password).encode(),bcrypt.gensalt())
            if User.objects.create(name=name, u_name=u_name, hashedpassword=pwhash):
                print "Reg Success"
                user = User.objects.last()
                return(flag,user)
            else:
                print "Reg Failed"
                return(flag,errors)
        return(flag, errors)
    def loginValidator(self, postData):
        try:

                 user= User.objects.get(u_name=postData['u_name'])
                 print "user", user
                 password = postData['password'].encode()
                 hashed = user.hashedpassword.encode()
                 if bcrypt.hashpw(password, hashed) == hashed :
                     return (True, user)
                 else:
                     return(False, "Login Credentials are invalid")

        except:
                     return(False, "Login Credentials are invalid " )
class User(models.Model):
    name = models.CharField(max_length= 50)
    u_name = models.CharField(max_length= 50)
    hashedpassword = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length= 50)
    description = models.CharField(max_length= 50)
    datefrom = models.CharField(max_length= 50)
    dateto = models.CharField(max_length= 50)
    owner = models.ForeignKey('User')

class Join(models.Model):
        user = models.ForeignKey('User', models.DO_NOTHING, related_name="user2user")
        trip = models.ForeignKey('Trip', models.DO_NOTHING, related_name="Trip2Trip")
