#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField
from Activities.models import Activity
class DiaryManager(models.Manager):
    def create_diary(self,title,content):
        diary = super(DiaryManager,self).create(
                title = title,
                content = content,
                )
        return diary
class Diary(models.Model):
	title=models.CharField(max_length=50,verbose_name='标题')
	content=RichTextField(verbose_name='内容')
	finished_time=models.DateTimeField(
                default = timezone.now,
                )
	public=models.BooleanField(
		verbose_name='公开',
		default=True,
		)

	author=models.ForeignKey(
                settings.AUTH_USER_MODEL,
                default=None,
                )
	act_belonged = models.ForeignKey(
				Activity,
				default =None,
				)
        objects = DiaryManager()
	def __unicode__(self):
		return self.title

	#set method
	def set_title(self,title):
            self.title = title

	def set_content(self,content):
	    self.content = content

	def be_friendly(self):
            self.friendly = True

	def de_friendly(self):
            self.friendly = False

	#get method
	def get_title(self):
            return self.title

	def get_content(self):
	    return self.content

	def get_finished_time(self):
            return self.finished_time

        @property
	def is_friendly(self):
            '''
            if the diary can be saw by friend
            '''
            return self.friendly
