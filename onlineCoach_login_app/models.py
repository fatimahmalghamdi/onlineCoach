from django.db import models
import datetime
import re


class UserManager(models.Manager):
    def basic_validate(self,postData):
        errors={}
        if len(postData.get('first_name'))<3:
            errors['first_name']="Sorry the First Name should be at least 3 Characters"
        elif len(postData.get('last_name'))<3:
            errors['last_name']="Sorry the Last Name should be at least 3 Characters"
        # elif postData["email"] <0:
        #     errors['email']="Sorry, you should enter the email !"
        elif len(postData.get('password'))<8:
            errors['password']="Sorry, The password should be at least 8 characters"
        elif postData.get('conf_password') != postData.get('password_confirm'):
            errors['conf_password']="Sorry, The password and the password Confirmation doesn't match" 
        elif (datetime.datetime.now().year - datetime.datetime.strptime(postData.get('birthdate')).year) < 13:
            errors['birthdate']="Sorry, You should be at least 13 years old to this website!"
        elif float(postData.get('height')) <=0.0:
            errors['height']="Sorry, the height could not be negative "
        elif float(postData.get('weight')) <=0.0:
            errors['weight']="Sorry, the weight could not be negative "

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address"
        else:
            try:
                User.objects.get(email=postData["email"])
                errors["email"] = "The email is already exists"
            except:
                pass
        
        return errors

    
    def basic_validate_coach(self, postData):
        errors={}
        if len(postData.get('desc')) < 8:
            errors['desc']="Sorry, the description should be at least 8 characters "
        return errors

        
    def validate_login(self, postData):
        login_errors= {}
        if len(postData.get('password'))<8:
            login_errors['password']="Sorry, The password should be at least 8 characters"
        # elif postData.get('email') <0:
        #     login_errors['email']="Sorry, you should enter the email !"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):
            login_errors["email"] = "Invalid email address"
        else:
            try:
                User.objects.get(email=postData["email"])
            except:
                pass
        return login_errors

            

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()
    # isCoach= models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects=UserManager()


class Coach(User):
    profile_pic = models.ImageField(upload_to='images/')
    brief = models.TextField()