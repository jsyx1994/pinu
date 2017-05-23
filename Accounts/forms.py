from django import forms
from captcha.fields import CaptchaField

class CapchaFieldForm(forms.Form):
	captcha = CaptchaField()