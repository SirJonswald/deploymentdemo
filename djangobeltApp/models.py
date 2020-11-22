from django.db import models
import bcrypt
import re
from datetime import date
# Create your models here.

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # ClassName.objects.exclude(field1="value for field1", etc.) - gets any records not matching the query provided
        usersWithSameEmail = User.objects.filter(email = postData['email'])
        print(f"users with the same email: {usersWithSameEmail}")
        errors = {}
        if len(postData['fname']) == 0:
            errors['fnamereq'] = "First Name is required"
        if len(postData['fname']) < 2:
            errors['fnamereq2char'] = "First Name requires at least 2 characters"
        if len(postData['lname']) == 0:
            errors['lnamereq'] = "Last Name is required"
        if len(postData['lname']) < 2:
            errors['lnamereq'] = "Last Name requires at least 2 characters"
        if len(postData['email']) == 0:
            errors['emailreq'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['emailpattern'] = "Email is not valid"
        elif len(usersWithSameEmail) >0:
            errors['emailtaken'] = "This email is already in use, choose a different email"
        if len(postData['pass']) == 0:
            errors['passreq'] = "Password is required"
        elif len(postData['pass']) <8:
            errors['passreqchar'] = "Password needs to be 8 characters or longer"
        if postData['pass'] != postData['cpw']:
            errors['cpwmatch'] = "Passwords must match!"
        return errors
    def loginValidator(self, postData):
        errors = {}
        usersWithSameEmail = User.objects.filter(email = postData['email'])
        if len(usersWithSameEmail) ==0:
            errors['emailnotfound'] = "This email is not yet registered. Please register first"
        else:
            matchUser = User.objects.get(email = postData['email'])
            if not bcrypt.checkpw(postData['pass'].encode(), matchUser.password.encode()):
                errors['incorrectpassword'] = "password is incorrect"
        return errors
class TripManager(models.Manager):
    def createTripValidator(self, postData):
        errors = {}
        today = str(date.today())
        if len(postData['tripName']) == 0:
            errors['tripnamerequired'] = "Destination is required"
        if len(postData['tripName']) < 2:
            errors['tnamereq2char'] = "Destination requires at least 2 characters"
        if len(postData['disc']) == 0:
            errors['discrequired'] = "Description is required"
        if len(postData['disc']) < 2:
            errors['discreq2char'] = "Descriptionrequires at least 2 characters"
        if len(postData['startDate']) == 0:
            errors['startdaterequired'] = "Expiration date is required"
        elif postData['startDate'] < today:
            errors['pastdate'] = "Cant plan trip in the past"
        if len(postData['endDate']) == 0:
            errors['enddaterequired'] = "Expiration date is required"
        elif postData['endDate'] < today:
            errors['pastdate'] = "Cant plan trip in the past"
        return errors

    def loginValidator(self, postData):
        errors = {}
        usersWithSameEmail = User.objects.filter(email = postData['email'])
        if len(usersWithSameEmail) ==0:
            errors['emailnotfound'] = "This email is not yet registered. Please register first"
        else:
            matchUser = User.objects.get(email = postData['email'])
            if not bcrypt.checkpw(postData['pass'].encode(), matchUser.password.encode()):
                errors['incorrectpassword'] = "password is incorrect"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Travel(models.Model):
    description = models.CharField(max_length = 255)
    plan = models.CharField(max_length = 255)
    creator = models.ForeignKey(User, related_name = 'trips_created', on_delete = models.CASCADE)
    favoritors = models.ManyToManyField(User, related_name = 'trips_favorited')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()