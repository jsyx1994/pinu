#coding:utf-8
from django import forms

class RegisterForm(forms.Form):
	USER_SEX = (
		('F','男'),
		('M','女'),
		)
	username = forms.EmailField(
		max_length = 100,
		label = 'Your email',
		)
	password = forms.CharField(
		max_length=100,
		widget=forms.PasswordInput,
		)
	nick_name = forms.CharField(
		max_length = 100,
		label = 'Your nick name',
		)
	real_name = forms.CharField(
		max_length = 50,
		label = 'Your real name',
		)
	sex = forms.ChoiceField(
		widget = forms.RadioSelect,
		choices = USER_SEX,
		label = 'Your sex',
		)
