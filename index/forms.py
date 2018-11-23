from django import forms
from .models import *

# class LoginForm(forms.Form):
#     uphone = forms.CharField(
#         label='手机号',
#         widget=forms.TextInput(
#             attrs={
#                 'class':'uText',
#             }
#         )
#     )
#     upwd = forms.CharField(
#         label='密码',
#         widget=forms.PasswordInput(
#             attrs={
#                 'placeholder':'请输入6-20位号码字符',
#                 'class':'uText',
#             }
#         )
#     )