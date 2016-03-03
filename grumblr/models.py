from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class UserInformation(models.Model):
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, default='')
    location = models.CharField(max_length=50, default='')
    school = models.CharField(max_length=50, default='')
    phoneNum = models.CharField(max_length=50, default='')
    avatar = models.ImageField(upload_to="avatar", default="avatar/default.jpg")
    short_bio = models.CharField(max_length=420, default='No instruction', blank=True)
    user = models.OneToOneField(User, related_name="information")
    follow = models.ManyToManyField(User, related_name="followed_by", blank=True)
    block = models.ManyToManyField(User, related_name="blocked_by", blank=True)
    token = models.CharField(max_length=100, default='')

    @staticmethod
    def get_userInfo(user):
        return UserInformation.objects.filter(user=user)

class Message(models.Model):
    text = models.CharField(max_length=42)
    timestamp = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to="picture", blank=True)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.text

class Comment(models.Model):
    writer = models.ForeignKey(User)
    text = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, related_name="comments", null=True)
    def __unicode__(self):
        return self.text
