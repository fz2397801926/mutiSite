from django import forms
from django.forms import fields
from ckeditor.fields import CKEditorWidget,RichTextField

# 登录表单
class LoginForm(forms.Form):
    email = fields.CharField(max_length=20,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder':'在此输入你的邮箱',
        }
    ))
    password = fields.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'密码',
        }
    ))
    remenber = fields.BooleanField(widget=forms.CheckboxInput(
        attrs={
            'class':'styled-checkbox',
            'id':'styled-checkbox-3',
        }
    ),required=False)

# 注册表单
class RegisterForm(forms.Form):

    nickname = forms.CharField(max_length=20,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'id':'signin_form',
            'placeholder':'昵称',
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'id': 'signin_form',
            'placeholder': '邮箱',
        }
    ))
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id': 'signin_form',
            'placeholder': '密码',
        }
    ))
    passwordConfirmed = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'signin_form',
            'placeholder': '请再次密码',
        }
    ))

    accept = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={

        }
    ))


    def clean__email(self):
        print('clean__email')

# 编辑表单
class EditForm(forms.Form):
    content = forms.CharField(widget=CKEditorWidget())