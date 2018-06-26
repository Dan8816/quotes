from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 :
            errors['first_name'] = "A valid first name is required"
        if not postData['first_name'].isalpha():
            errors['first_alpha'] = "First name cannot contain numbers or special characters"
        if len(postData['last_name']) < 2 :
            errors['last_name'] = "A valid last name is required"
        if not postData['last_name'].isalpha():
            errors['last_alpha'] = "Last name cannot contain numbers or special characters"
        if postData['password'] != postData['confirmpassword']:
            errors['pass_match'] = "Passwords do not match"
        if len(postData['password']) < 8 or len(postData['confirmpassword']) < 8:
            errors['pass_short'] = "Password must be more than 8 characters"
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "A valid email address is required"
        if User.objects.filter(email=postData['email']).exists():
            errors['email_reg'] = "This email address has already been registered"
        return errors        
    def update_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 :
            errors['first_name'] = "A valid first name is required"
        if not postData['first_name'].isalpha():
            errors['first_alpha'] = "First name cannot contain numbers or special characters"
        if len(postData['last_name']) < 2 :
            errors['last_name'] = "A valid last name is required"
        if not postData['last_name'].isalpha():
            errors['last_alpha'] = "Last name cannot contain numbers or special characters"
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "A valid email address is required"
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) < 2:
            errors['author'] = "Author must not be empty"
        if not postData['author'].isalpha():
            errors['author'] = "Author cannot contain spaces, numbers, or special characters"
        if len(postData['quote']) < 2:
            errors['quote'] = "Quote must not be empty"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 255)
    objects = UserManager()
    def __repr__(self):
        return "<user: {} | {}, {} >".format(self.id, self.first_name, self.last_name, self.email, self.password)

class Quote(models.Model):
    user = models.ForeignKey(User, related_name="post_quotes")
    quote = models.TextField(max_length=255)
    author = models.CharField(max_length=25)
    likes = models.ManyToManyField(User, related_name = "likes_quote")
    like_count = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = QuoteManager()
    def __repr__(self):
        return "<msg: {} | {} {}>".format(self.id, self.user, self.quote, self.author)


# Create your models here.
