from django.shortcuts import render, redirect, get_object_or_404
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.db import transaction
# Needed to manually create HttpResponses pr raise an Http404 exception
from django.http import HttpResponse, Http404, JsonResponse
from mimetypes import guess_type
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from time import time
from datetime import datetime
import pytz
from pytz import timezone
from django.db.models import Q
from grumblr.forms import *
from django.utils import formats


def check_login(request):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        return redirect(reverse('login'))


@login_required
def home(request):
    return global_stream(request, {})


def global_stream(request, args):
    all_follows = get_object_or_404(UserInformation, user=request.user).follow.all()
    block_users = []
    unfollow_users = []
    global_messages = []

    users1 = User.objects.exclude(
        Q(pk__in=request.user.information.follow.all()) | Q(pk__in=request.user.information.block.all())| Q(pk=request.user.id))
    for user in users1:
        user_info = get_object_or_404(UserInformation, user=user)
        if request.user not in user_info.block.all():
            unfollow_users.append(user)

    templates = 'grumblr/global_stream.html'

    all_blocks = User.objects.filter(pk__in=request.user.information.block.all())
    for block in all_blocks:
        block_users.append(block)

    messages = Message.objects.exclude(user__in=request.user.information.block.all()).order_by('-timestamp')
    for message in messages:
        user2_info = get_object_or_404(UserInformation, user=message.user)
        if request.user not in user2_info.block.all():
            global_messages.append(message)

    context = {"messages": global_messages, "user": request.user,
               "SearchUserForm": SearchUserForm(), "Unfollows": unfollow_users, "Blocks": block_users,
               "isFollow": "False"}
    context['update_time'] = time()
    context["CommentForm"] = CommentForm()
    context["Follows"] = all_follows
    context['stream'] = 'global'
    for key in args.keys():
        context[key] = args[key]
        if key == "isFollow" and args[key] == "True":
            context['stream'] = 'follower'
            templates = 'grumblr/follower_stream.html'
    return render(request, templates, context)


@login_required
@transaction.atomic
def follower_stream(request):
    context = {}
    context["isFollow"] = "True"
    follow_messages = []
    messages = Message.objects.filter(
        Q(user__in=request.user.information.follow.all()) | Q(user=request.user)).order_by('-timestamp')
    for message in messages:
        userInfo = get_object_or_404(UserInformation, user=message.user)
        if request.user not in userInfo.block.all():
            follow_messages.append(message)
    context["messages"] = follow_messages
    return global_stream(request, context)


@login_required
@transaction.atomic
def add_post(request):
    context = {}
    context["PostForm"] = PostForm()
    if 'marker' in request.POST:
        context["isFollow"] = "True"
    if request.method == 'GET':
        return global_stream(request, context)

    form = PostForm(request.POST, request.FILES)
    context["PostForm"] = form

    # Validates the form.
    if not form.is_valid():
        return global_stream(request, context)

    new_message = Message(user=request.user, text=request.POST['text'], img=request.FILES.get('img' ''))
    new_message.save()
    return global_stream(request, context)


@login_required
@transaction.atomic
def search_user(request):
    context = {}
    if 'marker' in request.POST:
        context["isFollow"] = "True"
    if request.method == 'GET':
        return global_stream(request, context)

    form = SearchUserForm(request.POST)
    context["SearchUserForm"] = form

    if not form.is_valid():
        return global_stream(request, context)

    searched = User.objects.get(username__exact=form.cleaned_data['search_name'])
    context["searched"] = searched
    return global_stream(request, context)


@login_required
@transaction.atomic
def profile(request, uid):
    if uid == str(request.user.id):
        return self_profile(request)
    else:
        post_user = get_object_or_404(User, pk=uid)
        userInfo = get_object_or_404(UserInformation, user=post_user)
        if request.user in userInfo.block.all():
            return block_profile(request, uid)
        else:
            return other_profile(request, uid)


def self_profile(request):
    context = {"messages": Message.objects.filter(user=request.user).order_by('-timestamp'),
               "post_user": request.user,
               "user": request.user}
    context['stream'] = 'profile'
    context['self'] = 'true'
    userInfo = get_object_or_404(UserInformation, user=request.user)
    context["CommentForm"] = CommentForm()
    context["UserInformationForm"] = EditInformationForm(instance=userInfo)
    return render(request, 'grumblr/self_profile.html', context)


def block_profile(request, uid):
    post_user = User.objects.get(id=uid)
    context = {"post_user": post_user, "user": request.user}
    context['self'] = 'false'
    return render(request, 'grumblr/block_profile.html', context)


def other_profile(request, uid):
    my_follows = get_object_or_404(UserInformation, user=request.user).follow.all()
    my_block = get_object_or_404(UserInformation, user=request.user).block.all()
    types = []
    post_user = User.objects.get(id=uid)
    if post_user not in my_follows:
        types.append("Unfollow")
    if post_user in my_follows:
        types.append("Followed")
    if post_user in my_block:
        types.append("Blocked")
    if post_user not in my_block:
        types.append("Unblock")
    context = {"messages": Message.objects.filter(user=post_user).order_by('-timestamp'),
               "post_user": post_user,
               "user": request.user}
    userInfo = get_object_or_404(UserInformation, user=post_user)
    context["UserInformationForm"] = EditInformationForm(instance=userInfo)
    context["CommentForm"] = CommentForm()
    context["types"] = types
    context['stream'] = 'profile'
    context['self'] = 'false'
    return render(request, 'grumblr/other_profile.html', context)


@login_required
@transaction.atomic
def delete_post(request, id):
    post_to_delete = get_object_or_404(Message, id=id)
    comment_to_delete = post_to_delete.comments.all()
    for comment in comment_to_delete:
        comment.delete()
    post_to_delete.delete()

    messages = Message.objects.filter(user=request.user).order_by('-timestamp')
    context = {"messages": messages, "post_user": request.user, "user": request.user}
    userInfo = get_object_or_404(UserInformation, user=request.user)
    context["UserInformationForm"] = EditInformationForm(instance=userInfo)
    return render(request, 'grumblr/self_profile.html', context)


@login_required
@transaction.atomic
def edit_profile(request):
    gender = ['Male', 'Female', 'male', 'female', 'FEMALE', 'MALE']
    context = {'user': request.user, "userInfo": request.user.information}
    user_to_edit = get_object_or_404(User, pk=request.user.id)
    userInfo_to_edit = get_object_or_404(UserInformation, user=request.user)

    if request.method == 'GET':
        context["EditInformationForm"] = EditInformationForm(instance=userInfo_to_edit, prefix='EditInformationForm')
        context["EditUserForm"] = EditUserForm(instance=user_to_edit, prefix='EditUserForm')
        return render(request, 'grumblr/edit_profile.html', context)

    form = EditInformationForm(request.POST, request.FILES, instance=userInfo_to_edit, prefix='EditInformationForm')
    form2 = EditUserForm(request.POST, instance=user_to_edit, prefix='EditUserForm')
    context["EditInformationForm"] = form
    context["EditUserForm"] = form2
    if not form2.is_valid():
        return render(request, 'grumblr/edit_profile.html', context)
    if not form.is_valid():
        return render(request, 'grumblr/edit_profile.html', context)

    if form2.cleaned_data['username'] != request.user.username and len(
            User.objects.filter(username=form2.cleaned_data['username'])) > 0:
        context['UserNameError'] = 'Username is already taken.'
        return render(request, 'grumblr/edit_profile.html', context)
    if not form.cleaned_data['gender'] in gender:
        context['GenderError'] = "Invalid input! Valid choice:'Male,Female,male,female,MALE,FEMALE'"
        return render(request, 'grumblr/edit_profile.html', context)
    form.save()
    form2.save()
    context["success"] = "Update your profile successfully!"
    return render(request, 'grumblr/edit_profile.html', context)


@login_required
@transaction.atomic
def change_password(request):
    context = {"user": request.user, "userInfo": request.user.information}
    context["ChangePasswordForm"] = ChangePasswordForm()
    templates = "grumblr/change_password.html"
    if request.method == 'GET':
        return render(request, templates, context)

    form = ChangePasswordForm(request.POST)
    context["ChangePasswordForm"] = form
    if not form.is_valid():
        return render(request, 'grumblr/change_password.html', context)

    errors = []
    if not request.user.check_password(form.cleaned_data['password1']):
        errors.append("The Password is not correct.")
        context["errors"] = errors
        return render(request, 'grumblr/change_password.html', context)
    else:
        request.user.set_password(form.cleaned_data['new_password'])
        request.user.save()
        return redirect('/grumblr/')


@transaction.atomic
def registration(request):
    context = {}
    context["RegisterForm"] = RegisterForm()
    if request.method == 'GET':
        return render(request, 'grumblr/registration.html', context)

    form = RegisterForm(request.POST, request.FILES)
    context["RegisterForm"] = form

    if not form.is_valid():
        return render(request, 'grumblr/registration.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        last_name=form.cleaned_data['last_name'],
                                        first_name=form.cleaned_data['first_name'],
                                        email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password1'])
    new_user.save()
    new_userInfo = UserInformation(user=new_user)
    new_userInfo.save()
    new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect('/grumblr/')


@login_required
@transaction.atomic
def get_avatar(request, uid):
    userInfo = get_object_or_404(UserInformation, id=uid)
    if not userInfo.avatar:
        raise Http404
    content_type = guess_type(userInfo.avatar.name)
    return HttpResponse(userInfo.avatar, content_type=content_type)


@login_required
@transaction.atomic
def upload_picture(request, id):
    messagePic = get_object_or_404(Message, id=id)
    if not messagePic.img:
        raise Http404
    content_type = guess_type(messagePic.img.name)
    return HttpResponse(messagePic.img, content_type=content_type)


@login_required
def follow_user(request, uid):
    user = get_object_or_404(User, id__exact=uid)
    errors = []
    # follow --> unfollow
    if user in request.user.information.follow.all():
        request.user.information.follow.remove(user)
    else:
        # block --> follow
        if user in request.user.information.block.all():
            context = {'errors': errors}
            return redirect('/grumblr/profile/%s' % uid, context)
        else:
            # unblock//unfollow --> follow
            request.user.information.follow.add(user)
    request.user.save()
    return redirect(reverse('profile', args=uid))


@login_required
def block_user(request, uid):
    user = get_object_or_404(User, id__exact=uid)
    # block --> unblock
    if user in request.user.information.block.all():
        request.user.information.block.remove(user)
    else:
        # unblock --> unblock
        if user in request.user.information.follow.all():
            request.user.information.follow.remove(user)
        request.user.information.block.add(user)
    request.user.save()
    return redirect(reverse('profile', args=uid))


def send_email(request):
    context = {}
    context["SendEmailForm"] = SendEmailForm()
    if request.method == 'GET':
        return render(request, 'grumblr/send_email.html', context)
    form = SendEmailForm(request.POST)
    context["SendEmailForm"] = form
    if not form.is_valid():
        return render(request, 'grumblr/send_email.html', context)
    user = get_object_or_404(User, email=form.cleaned_data['email'])
    token = default_token_generator.make_token(user)
    userInfo = get_object_or_404(UserInformation, user=user)
    userInfo.token = token
    userInfo.save()
    email_body = "Please visit http://127.0.0.1:8000/grumblr/reset_password?token=%s to set your password." % token

    send_mail(subject='Reset Your Grumblr Password',
              message=email_body,
              from_email='panli@andrew.cmu.edu',
              recipient_list=[user.email])
    context["email"] = form.cleaned_data['email']
    context["success"] = "The reset email has sent. Please check!"
    return render(request, 'grumblr/send_email.html', context)


def reset(request):
    context = {}
    if request.method == "GET":
        token = request.GET["token"]
        context["ResetPasswordForm"] = ResetPasswordForm()
        context["token"] = token
        return render(request, 'grumblr/reset_password.html', context)

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        context["ResetPasswordForm"] = form
        token = request.POST["token"]
        user = UserInformation.objects.get(token__exact=token).user

        context["token"] = token

        if not form.is_valid():
            return render(request, 'grumblr/reset_password.html', context)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return redirect('/grumblr/')


@login_required
@transaction.atomic
def update_stream(request):
    if not 'time' in request.GET or not request.GET['time']:
        return HttpResponse('error')
    last_update = datetime.fromtimestamp(float(request.GET['time']), pytz.UTC)
    json = {'update_time': time()}
    messages = []
    # get new grumblr list
    new_message = Message.objects.all().filter(timestamp__gt=last_update).order_by('timestamp')
    eastern = timezone('US/Eastern')
    my_follow = get_object_or_404(UserInformation, user=request.user).follow.all()
    for message in new_message:
        m = {}
        if message.user in my_follow:
            m["isFollow"] = "True"
        else:
            m["isFollow"] = "False"
        m['mid'] = message.id
        m['user_name'] = message.user.username
        m['user_id'] = message.user.id
        m['timestamp'] = formats.date_format(message.timestamp.astimezone(eastern), "DATETIME_FORMAT")

        m['length'] = len(message.comment.all())
        m['text'] = message.text
        if message.img is None:
            m['img'] = ""
        else:
            m['img'] = message.img.name
        messages.append(m)

    json['messages'] = messages
    return JsonResponse(json)


@login_required
@transaction.atomic
def comment(request, id):
    context = {}
    current_message = get_object_or_404(Message, id=id)
    eastern = timezone('US/Eastern')
    if request.is_ajax():
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment(message=current_message,writer=request.user, text=request.POST['text'])
            new_comment.save()
            time = formats.date_format(Comment.objects.latest('timestamp').timestamp.astimezone(eastern),
                                       "DATETIME_FORMAT")
            context = {"comment": form.cleaned_data["text"], "writer_name": request.user.username, "time": time,
                       "number": len(current_message.comments.all()), "error": "false", "writer_id": request.user.id}
            return JsonResponse(context)
        else:
            context = {"error": "true"}
            return JsonResponse(context)
    form = CommentForm(request.POST)
    if not form.is_valid():
        return global_stream(request, context)
    new_comment = Comment(message=current_message,writer=request.user, text=request.POST['text'])
    new_comment.save()
    return global_stream(request, context)


@login_required
@transaction.atomic
def get_comments(request, id):
    eastern = timezone('US/Eastern')
    message = get_object_or_404(Message, id=id)
    comments = message.comments.order_by("timestamp")
    json = {}
    json['comments'] = []
    for comment in comments:
        time = formats.date_format(comment.timestamp.astimezone(eastern), "DATETIME_FORMAT")
        c = {'uid': comment.writer.id,
             'username': comment.writer.username,
             'text': comment.text,
             'time': time}
        json['comments'].append(c)
    return JsonResponse(json)
