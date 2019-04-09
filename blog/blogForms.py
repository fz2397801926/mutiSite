from django import forms
from django.forms import fields

class LoginForm(forms.Form):
    username = fields.CharField(max_length=20,widget=forms.TextInput(
        attrs={'class':'form-control',}
    ))
    password = fields.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',}
    ))

class RegisterForm(forms.Form):
    gender = {
        (0, '保密'),
        (1, '男'),
        (2, '女'),
    }

    username = forms.CharField(max_length=20,widget=forms.TextInput(
        attrs={'class':'form-control',}
    ))
    password = forms.CharField(max_length=20,widget=forms.TextInput(
        attrs={'class':'form-control',}
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class':'form-control',}
    ))
    sex = forms.IntegerField(widget=forms.Select(
        choices=gender,
        attrs={
            'class':'form-control',
        }
    ))


    def clean__email(self):
        print('clean__email')