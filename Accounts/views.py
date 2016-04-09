#coding:utf-8
from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import MyUser as User
def index(request):
    if not request.user.is_authenticated():
        user = None
    else:
        user = request.user
    return render(request,'base.html',{'user':user})

def register(request):
    if request.method == 'POST':
        post = request.POST
        email = post['email']
        password = post['password1']
        real_name = post['first_name']+post['last_name']
        nick_name =post['nick_name']
        sex = post['sex']
        phone_num = post['phone_num']
        try:
            User.objects.create_user(
                email = email,
		        password = password,
		        nick_name = nick_name,
		        real_name = real_name,
                phone_num = phone_num,
                sex = sex,
            )
        except:
            return HttpResponse('nick_name or email already be taken')
        return render(request,'accounts/login.html')
    else:
        #form = RegisterForm()
        return render(request,'accounts/register.html')

def log_in(request):
    user = None
    if request.method == 'POST':
        email = request.POST['email']
    	password = request.POST['password']
    	user = authenticate(
        	username = email,
        	password = password,
            )
    	if user is not None:
            if user.is_active:
    	        login(request,user)
                user.set_lng(request.POST['lng'])
                user.set_lat(request.POST['lat'])
                #should check if the location is changed
                if user.get_last_login_city() != request.POST['city']:
                    pass
                user.set_last_login_city(request.POST['city'])
                user.set_online()
                user.save()
                return redirect('index')
    	    else:
    		    pass
    	else:
            return render(request,'accounts/login.html',{'error':'账户或密码错误'})
    else:
        return render(request,'accounts/login.html',{'user':user})

@login_required
def user_info(request):
    user = request.user
    context = {
            'sex':user.get_sex(),
            'real_name':user.get_real_name(),
            'nick_name':user.get_nick_name(),
            'email':user.get_email(),
            'work':user.get_work(),
            'phone_num':user.get_phone_num(),
            'weight':user.get_weight(),
            'height':user.get_height(),
            'age':user.get_age(),
            }
    return render(request,'accounts/user_info.html',context)

@login_required
def info_edit(request):
    user = request.user
    if request.method == 'POST':
        post=request.POST
        nn=post['nick_name']
        em=post['email']
        wk=post['work']
        pn=post['phone_num']
        user.set_nick_name(nn)
        user.set_email(em)
        user.set_work(wk)
        user.set_phone_num(pn)
        user.save()
        return HttpResponse('ok')
    else:
        context = {
                'sex':user.get_sex(),
                'real_name':user.get_real_name(),
                'nick_name':user.get_nick_name(),
                'email':user.get_email(),
                'work':user.get_work(),
                'phone_num':user.get_phone_num(),
                'weight':user.get_weight(),
                'height':user.get_height(),
                'age':user.get_age(),
                'friend_list':user.friends.all(),
                }
        return render(request,'accounts/info_edit.html',context)

@login_required
def log_out(request):
    request.user.set_offline()
    request.user.save()
    logout(request)
    return render(request,'base.html',{'user':None})

def fri_detail(request):
    pass
