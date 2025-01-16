from django import forms
from tweets.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','username','first_name','last_name','phone_number','dob','profile_photo','bio','gender']
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'dob': forms.DateInput(attrs={'class':'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
        }