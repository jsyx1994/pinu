#!coding:utf-8
from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from .models import Diary

class PostForm(forms.ModelForm):
	content = forms.CharField(label = '',widget = CKEditorWidget())
	class Meta:
		model = Diary
		fields = ('title','content','public')

class PostAdmin(admin.ModelAdmin):
	form = PostForm

#admin.site.register(Diary, PostAdmin)