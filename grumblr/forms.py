from django import forms
from models import *
from django.contrib.auth.models import User
from localflavor.us.forms import USPhoneNumberField


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'label': 'Username', 'placeholder': 'Enter Username'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'label': 'First Name', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'label': 'Last Name', 'placeholder': 'Enter Last Name'}))
    email = forms.EmailField(max_length=100,
                             widget=forms.EmailInput(attrs={'label': 'Email', 'placeholder': 'Enter Email'}))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'label': 'Password', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'label': 'Confirm Password', 'placeholder': 'Re-Enter Password'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")
        return email


class EditInformationForm(forms.ModelForm):
    phoneNum = USPhoneNumberField(widget=forms.TextInput(attrs={'label': 'Phone#', 'class': 'form-control','pic': 'glyphicon glyphicon-phone'}))

    class Meta:
        model = UserInformation
        exclude = ('user', 'follow', 'block','token',)
        widgets = {'age': forms.NumberInput(
            attrs={'label': 'Age', 'class': 'form-control', 'pic': 'glyphicon glyphicon-heart'}),
                   'gender': forms.TextInput(
                       attrs={'label': 'Gender', 'class': 'form-control', 'pic': 'glyphicon glyphicon-tasks'}),
                   'location': forms.TextInput(
                       attrs={'label': 'Location', 'class': 'form-control', 'pic': 'glyphicon glyphicon-map-marker'}),
                   'school': forms.TextInput(
                       attrs={'label': 'School', 'class': 'form-control', 'pic': 'glyphicon glyphicon-envelope'}),
                   'avatar': forms.ClearableFileInput(
                       attrs={'label': 'Avatar', 'class': 'form-control', 'pic': 'glyphicon glyphicon-picture'}),
                   'short_bio': forms.Textarea(
                       attrs={'label': 'Biography', 'class': 'form-control', 'pic': 'glyphicon glyphicon-star'})}


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {'username': forms.TextInput(
            attrs={'label': 'Username', 'class': 'form-control', 'pic': 'glyphicon glyphicon-envelope'}),
                   'first_name': forms.TextInput(
                       attrs={'label': 'First Name', 'class': 'form-control', 'pic': 'glyphicon glyphicon-envelope'}),
                   'last_name': forms.TextInput(
                       attrs={'label': 'Last Name', 'class': 'form-control', 'pic': 'glyphicon glyphicon-envelope'})}


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'label': 'Old Password', 'type': 'password', 'placeholder': 'Enter Previous Password'}))
    new_password = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'label': 'New Password', 'type': 'password', 'placeholder': 'Enter New Password'}))
    re_password = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'label': 'Confirm Password', 'type': 'password', 'placeholder': 'Re-Enter New Password'}))

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        new_password = cleaned_data.get('new_password')
        re_password = cleaned_data.get('re_password')
        if new_password and re_password and new_password != re_password:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data


class SearchUserForm(forms.Form):
    search_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'label': 'Search By Name', 'type': 'text', 'placeholder': "Search Grumblr"}))

    def clean(self):
        cleaned_data = super(SearchUserForm, self).clean()
        return cleaned_data

    def clean_search_name(self):
        search_name = self.cleaned_data.get('search_name')
        if not User.objects.filter(username__exact=search_name):
            raise forms.ValidationError("No such a grumblr user.")
        return search_name

class SendEmailForm(forms.Form):
    email = forms.EmailField(max_length=100,
                             widget=forms.EmailInput(attrs={'label': 'Email', 'placeholder': 'Enter Email'}))

    def clean(self):
        cleaned_data = super(SendEmailForm, self).clean()
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__exact=email):
            raise forms.ValidationError("This email does not exist!")
        return email

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'label': 'Password', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'label': 'Confirm Password', 'placeholder': 'Re-Enter Password'}))

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

class PostForm(forms.Form):
    text = forms.CharField(max_length=42, widget=forms.Textarea(
        attrs={'placeholder': "What's on your mind?"}))
    img = forms.ImageField(required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('writer','message',)
        widgets = {forms.Textarea(
                       attrs={'class': 'form-control', 'placeholder': 'Type your comment'}),}
