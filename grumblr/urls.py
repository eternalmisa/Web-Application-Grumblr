"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'grumblr.views.home',name='home'),
   # Route for built-in authentication with our own custom login page
    # url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'grumblr/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^registration$', 'grumblr.views.registration', name='registration'),
    url(r'^global_stream$', 'grumblr.views.home', name='global_stream'),
    url(r'^follower_stream$', 'grumblr.views.follower_stream', name='follower_stream'),
    url(r'^add_post$', 'grumblr.views.add_post', name='add'),
    url(r'^delete_post/(?P<id>\d+)$', 'grumblr.views.delete_post',name='delete'),
    url(r'^profile/(?P<uid>\d+)$', 'grumblr.views.profile',name='profile'),
    url(r'^edit_profile$', 'grumblr.views.edit_profile', name='edit'),
    url(r'^change_password$', 'grumblr.views.change_password',name='change_password'),
    url(r'^search_user$', 'grumblr.views.search_user',name='search'),
    url(r'^media/avatar/(?P<uid>\d+)$', 'grumblr.views.get_avatar',name='avatar'),
    url(r'^media/picture/(?P<id>\d+)$', 'grumblr.views.upload_picture',name='upload_picture'),
    url(r'^follow/(?P<uid>\d+)$', 'grumblr.views.follow_user',name='follow_user'),
    url(r'^block/(?P<uid>\d+)$', 'grumblr.views.block_user',name='block_user'),
    url(r'^login$', 'grumblr.views.check_login',name='check_login'),
    url(r'^unlogin$', 'django.contrib.auth.views.login', {'template_name':'grumblr/login.html'}, name='login'),
    url(r'^send_email$', 'grumblr.views.send_email',name='send_email'),
    url(r'^reset_password$', 'grumblr.views.reset',name='reset'),
    url(r'^update_stream$', 'grumblr.views.update_stream'),
    url(r'^comment/(?P<id>\d+)$', 'grumblr.views.comment', name = "comment"),
    url(r'^get-comments/(?P<id>\d+)$', 'grumblr.views.get_comments'),
]
