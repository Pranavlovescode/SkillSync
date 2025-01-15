from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='username')
    password = forms.CharField(widget=forms.PasswordInput,label='password')


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, label='username')
    password = forms.CharField(widget=forms.PasswordInput,label='password')
    email = forms.EmailField(max_length=100,label='email')
    first_name = forms.CharField(max_length=100,label='first_name')
    last_name = forms.CharField(max_length=100,label='last_name')


