#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import(
	BaseUserManager,AbstractBaseUser
	)
from Activities.models import Activity
from Messages.models import Message
from Diaries.models import Diary
from haversine import calc_dis
from django.conf import settings
from datetime import date
import os
class MyUserManager(BaseUserManager):
    def create_user(self,email,nick_name,real_name,sex,password=None,phone_num=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nick_name=nick_name,
            real_name=real_name,
            phone_num = phone_num,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,nick_name,real_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            nick_name=nick_name,
	        real_name=real_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    #longtitude
    lng = models.FloatField(
        default = None,
        null = True,
        blank =True,
        )
    #latitude
    lat = models.FloatField(
        default = None,
        null = True,
        blank = True,
        )
    last_login_city = models.CharField(
        max_length = 20,
        blank = True,
        )
    USER_SEX = (
    	('M','男'),
    	('F','女'),
    	)
    email = models.EmailField(
    	verbose_name='email address',
    	max_length=255,
    	unique=True,
    	)
    profile = models.ImageField(
            upload_to = 'profiles',
            default = os.path.join(settings.MEDIA_URL,'profiles','default_profile.jpg')
            #null = True,
            #blank = True
            )
    address = models.CharField(
        max_length = 100,
        blank = True,
        )
    sex = models.CharField(
    	max_length = 1,
    	choices = USER_SEX,
    	default = 'M',
    	)
    nick_name = models.CharField(
    	#primary_key = True,
    	unique = True,
        max_length = 100,
    	)
    work = models.CharField(
    	max_length = 20,
    	blank = True,
    		)
    phone_num = models.CharField(
    	max_length = 15,
               # unique = True,通过后台来验证
    	blank = True,
                null = True,
    	)
    height = models.PositiveSmallIntegerField(
    	blank=True,
    	null = True,
    	)
    weight = models.PositiveSmallIntegerField(
    	blank=True,
    	null =True,
    	)
    birthday = models.DateField(
    	blank=True,
    	null = True,
    	)
    real_name = models.CharField(
    	#unique = True,
    	max_length = 100,
    	)
    online = models.NullBooleanField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
    	'nick_name',
    	'real_name',
        'sex',
    	]

    friends=models.ManyToManyField(
    	'self',
    	related_name = 'friShip',
    	through = 'FriendShip',
    	through_fields = ('subject','friend'),
    	symmetrical=False,
    	)
    def get_frist_name(self):
        return self.real_name[0]
    def get_full_name(self):
    	# The user is identified by their email address
        return self.real_name
    def get_short_name(self):
    	# The user is identified by their email address
        return self.nick_name
    def __unicode__(self):              # __unicode__ on Python 2
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin
        #above are the basic methods


    #Set method
    def set_last_login_city(self,city):
        self.last_login_city = city

    #if the user's longtitude or latitude can't be reached, then do nothing
    def set_lng(self,lng):
        try:
            self.lng = lng
        except Exception, e:
            self.lng = -360
    def set_lat(self,lat):
        try:
            self.lat = lat
        except Exception, e:
            self.lat = -360
    def set_real_name(self,real_name):
        self.real_name = real_name

    def set_nick_name(self,nick_name):
        self.nick_name = nick_name

    def set_sex(self,choice):
        self.sex = unicode(choice)

    def set_birthday(self,year,month,day):
        self.birthday = date(year,month,day)
        #self.birthday.year = year,
        #self.birthday.month = month,
        #self.birthday.day = day,

    def set_work(self,work):
        self.work = work

    def set_email(self,email):
        self.email = email

    def set_pswd(self,raw_password):
        self.set_password(raw_password)

    def set_profile(self,profile):
        self.profile = profile

    def set_phone_num(self,phone_num):
        self.phone_num = phone_num

    def set_height(self,height):
        self.height = height

    def set_weight(self,weight):
        self.weight = weight
    def set_address(self,address):
        self.address = address
    def set_online(self):
        self.online = True

    def set_offline(self):
        self.online = False
    
    #Get method
    def get_last_login_city(self):
        return self.last_login_city
    def get_lng(self):
        return self.lng
    def get_lat(self):
        return self.lat
    def get_real_name(self):
        return self.real_name

    def get_nick_name(self):
        return self.nick_name

    def get_sex(self):
            return self.get_sex_display()

    def get_age(self):
        date_of_birth=self.get_birthday()
        if date_of_birth :
            now = timezone.now()
            age = now.year - date_of_birth.year
            delta = now.month - date_of_birth.month
            if delta <0:
                age -= 1
            return age
        else:
            pass

    def get_birthday(self):
        if self.birthday :
            return self.birthday
        else:
            return ''

    def get_work(self):
        return self.work

    def get_email(self):
        return self.email

        #见密码管理http://python.usyiyi.cn/django_182/topics/auth/passwords.html
    def get_pswd():
            pass

    def get_profile(self):
        return self.profile.url

    def get_phone_num(self):
        if self.phone_num:
            return self.phone_num
        else:
            return ''
    def get_height(self):
        if self.height:
            return self.height
        else:
            return ''
    def get_weight(self):
        if self.weight:
            return self.weight
        else:
            return ''
    def get_address(self):
        return self.address
    @property
    def is_online(self):
        return self.online

    #通过id来添加好友,返回是否添加成功
    def add_friend(self,id):
        #check if subject already add the friend
        try:
            obj = MyUser.objects.get(id = id)
            # if not added yet then....
            assert len(FriendShip.objects.filter(subject = self,friend = obj)) == 0
        except MyUser.DoesNotExist:
            #print 'not'
            return False
        except AssertionError:
            #print 'ass'
            return False
        else:
            FriendShip.objects.create_friendship(self,obj)
            return True

    #通过id来删除好友,返回是否成功
    def del_friend(self,id):
        try:
            friend = MyUser.objects.get(id = id)
            fri = FriendShip.objects.get(subject = self,friend = friend)
        except FriendShip.DoesNotExist:
            return False
        else:
            fri.delete()
            return True

    def invite_friend(self):
        pass

    def join_act(self,pk):
        '''
        join the activity via its primary key(id)
        '''
        try:
            obj = Activity.objects.get(pk = pk)
        except Activity.DoesNotExist:
            return False
        else:
            stime = obj.get_start_time()
            etime = obj.get_due_time()
            act = Activity.objects.filter(person_joined = self)
            for i in act:
                if (stime < i.get_start_time() and etime > i.get_due_time()) or (i.get_start_time() < stime < i.get_due_time()) or (i.get_start_time() < etime < i.get_due_time()):
                    return False
            obj.person_joined.add(self)
            return True

    def quit_act(self,act_pk):
        try:
            obj = Activity.objects.get(pk = act_pk)
        except Activity.DoesNotExist:
            return False
        else:
            obj.person_joined.remove(self)
            return True

    def nearby_person(self,accuracy = 5000):
        '''
        return a list of nearby person,accuracy(meter)
        '''
        lng1 = self.get_lng();
        lat1 = self.get_lat();
        person_list = filter(
            lambda x: ( calc_dis(lng1=lng1,lat1=lat1,lng2=x.get_lng(),lat2=x.get_lat()) ) < accuracy,
            MyUser.objects.all()
            )
        return person_list
        
    def nearby_act(self,accuracy = 5000):
        '''
        return a list of nearby activity
        '''
        lng1 = self.get_lng();
        lat1 = self.get_lat();
        act_list = filter(
            lambda x: (( calc_dis(lng1=lng1,lat1=lat1,lng2=x.get_dlng(),lat2=x.get_dlat()) ) < accuracy)
                        or (( calc_dis(lng1=lng1,lat1=lat1,lng2=x.get_slng(),lat2=x.get_slat()) ) < accuracy),
            Activity.objects.get_valid_activity()
            )
        return act_list

    def nearby_advocator_act(self,accuracy = 5000):
        '''
        return a list of the activity via the distance between advocator and you
        '''
        lng1 = self.get_lng();
        lat1 = self.get_lat();
        act_list = filter(
            lambda x: ( calc_dis(lng1=lng1,lat1=lat1,lng2=x.advocator.get_lng(),lat2=x.advocator.get_lat()) ) < accuracy,
            Activity.objects.get_valid_activity()
            )
        return act_list

    def send_message(self,title,id,message = 'untitled'):
        obj = MyUser.objects.get(id = id)
        Message.objects.create_message(
                title = title,
                message = message,
                sender = self,
                receiver = obj,
                )

    def delete_message(self,pk):
        try:
            obj = Message.objects.get(pk = pk)
        except Message.DoesNotExist:
            return False
        else:
            if self == obj.sender:
                obj.seder_preserved = False
            elif self == obj.receiver:
                obj.rcver_preserved = False
            else:
                pass
            obj.save(update_fields = ['seder_preserved','rcver_preserved'])
            return True

    def keep_diary(self,title,content):
        diary = Diary.objects.create_diary(
                title = title,
                content = content,
                )
        diary.author = self

class FriendManager(models.Manager):
    def create_friendship(self,subject,friend):
        #check if subject already add the friend
        fri = super(FriendManager,self).create(
                subject = subject,
                friend = friend,
                )
        fri.save(using=self._db)
        if self.is_abs_friend_each_other(subject,friend):
            x = FriendShip.objects.get(subject = subject,friend = friend )
            x.friend_each_other = True
            x.save(update_fields=['friend_each_other'])
            x = FriendShip.objects.get(subject = friend,friend = subject )
            x.friend_each_other = True
            x.save(update_fields=['friend_each_other'])
        return fri

    def is_abs_friend_each_other(self,sub,obj):
        return ((sub in obj.friends.all()) and (obj in sub.friends.all()))

class FriendShip(models.Model):
    subject = models.ForeignKey(
        MyUser,
        related_name = 'subject',
        )
    friend = models.ForeignKey(
        MyUser,
        related_name = 'friend',
        )
    level = models.PositiveSmallIntegerField(
        default = 0
        )
    #is 's' a friend of 'o'? obviously initiate it with Default false
    friend_each_other = models.BooleanField(default = False)

    objects=FriendManager()
    def __unicode__(self):
        return self.subject.nick_name+u'\'s friend'

    def get_level(self):
        return self.level

    @property
    def is_friend_each_other(self):
        return self.friend_each_other
