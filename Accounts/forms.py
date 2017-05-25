#coding:utf-8
from django import forms
from captcha.fields import CaptchaField

class CapchaFieldForm(forms.Form):
	captcha = CaptchaField(label='验证码')