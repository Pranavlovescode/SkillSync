from django import forms

class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=100, label='username')
    password = forms.CharField(widget=forms.PasswordInput, label='password')

    def clean_username_or_email(self):
        data = self.cleaned_data['username_or_email']
        if '@' in data:
            if not forms.EmailField().clean(data):
                raise forms.ValidationError("Enter a valid email address.")
        return data


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, label='username')
    password = forms.CharField(widget=forms.PasswordInput,label='password')
    email = forms.EmailField(max_length=100,label='email')
    first_name = forms.CharField(max_length=100,label='first_name')
    last_name = forms.CharField(max_length=100,label='last_name')


