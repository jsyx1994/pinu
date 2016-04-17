#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.conf import settings
from django.utils import timezone
class ActivityManager(models.Manager):
    def create_activity(self,advocator,title,category,start_time,due_time,person_num_limit):
        activity = super(ActivityManager,self).create(
                title = title,
                category = category,
                start_time = start_time,
                due_time = due_time,
                person_num_limit = person_num_limit,
                advocator = advocator,
                )
        activity.save()
        return activity
    def get_valid_activity(self):
        list = filter(lambda a:a.is_valid,
                super(ActivityManager,self).all()
                )
        return list
class Activity(models.Model):
	#各种类型的活动，一级活动下可以再分二级。。。。。。
    CATEGORY_LIST=(
		('SP','运动'),
		('EN','娱乐'),
		('TR','旅行'),
	)
    #start position of an activity(optional)
    slng = models.FloatField(
        default = None,
        null = True,
        blank = True,
        )
    slat = models.FloatField(
        default = None,
        null = True,
        blank = True,
        )
    #destination of an activity
    dlng = models.FloatField(
        default = None,
        null = True,
        blank = True,
        )
    dlat = models.FloatField(
        default = None,
        null = True,
        blank = True,
        )
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=2,choices=CATEGORY_LIST)

    #用户所设定的开始时间
    start_time = models.DateTimeField()

    #用户所设定的结束时间
    due_time = models.DateTimeField()

    #自动设定的发布时间，用于检查新旧，默认为对象被创建的时间
    pub_time = models.DateTimeField(
                default = timezone.now,
                )

    #人数限制
    person_num_limit = models.PositiveSmallIntegerField()

    st_place = models.CharField(
        max_length = 100,
        blank = True,
        )
    ds_place =  models.CharField(
        max_length = 100,
        blank = True
        )
    advocator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name = 'advocator',
        default = None,
    )
    person_joined=models.ManyToManyField(
                settings.AUTH_USER_MODEL,
                related_name = 'person_joined',
                default = None,
                blank = True,
                )
    objects = ActivityManager()

    def __unicode__(self):
        return self.title

    #set method
    def set_slng(self,slng):
        self.slng = slng
    def set_slat(self,slat):
        self.slat = slat
    def set_dlng(self,dlng):
        self.dlng = dlng
    def set_dlat(self,dlat):
        self.dlat = dlat
    def set_title(self,title):
	    self.title = title
    def set_st_place(self,st_place):
        self.st_place = st_place
    def set_ds_place(self,ds_place):
        self.ds_place = ds_place
    def set_category(self,category):
        self.category = category
    def set_start_time(self,start_time):
        self.start_time = start_time
    def set_due_time(self,duetime):
	    self.start_time = due_time
    
    #get method
    def get_slat(self):
        if self.slat:
            return self.slat
        else:
            return -360
    def get_slng(self):
        if self.slng:
            return self.slng
        else:
            return -360
    def get_dlat(self):
        if self.dlat:
            return self.dlat
        else:
            return -360
    def get_dlng(self):
        if self.dlng:
            return self.dlng
        else :
            return -360
    def get_title(self):
        return self.title
    def get_st_place(self):
        return self.st_place
    def get_ds_place(self):
        return self.ds_place
    def get_pub_time(self):
	    return self.pub_time

        #活动进行的时间
    def get_time_last(self):
	    return self.get_due_time() - self.get_start_time()

        #参与活动的剩余时间
    def get_time_left(self):
		return self.get_due_time() - timezone.now()

    def get_rest_time(self):
        return self.get_start_time() - timezone.now()

    def get_start_time(self):
	    return self.start_time

    def get_due_time(self):
	    return self.due_time

    def get_startDpub_time(self):
        return self.get_start_time() - self.get_pub_time()

    def get_person_num(self):
		return self.person_num_limit

    @property
    def get_category(self):
        return self.get_category_display()
   
    #是否可参与,人数未满并且在可参与的时间段
    @property
    def is_active(self):
        return self.get_pub_time() < timezone.now() < self.get_start_time()
    
    @property
    def is_valid(self):
        time_ok = self.get_pub_time() < timezone.now() < self.get_start_time()
        num_ok = not self.is_full
        return (time_ok and num_ok)

    #是否在进行中
    @property
    def is_going(self):
        return self.get_start_time() < timzone.now() < self.get_due_time()

    #是否已满
    @property
    def is_full(self):
        return self.get_person_num() == self.person_joined.count()

    #是否已到期
    @property
    def is_due(self):
        return timezone.now() > self.get_due_time()
