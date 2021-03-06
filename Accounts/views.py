#coding:utf-8
from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse,Http404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import MyUser as User
from Accounts.haversine import calc_dis
from Messages.models import * 
from django.core.mail import send_mail
from random import sample
from django.shortcuts import get_object_or_404
from Accounts.models import MyUser
from django.conf import settings
from .forms import CapchaFieldForm
from django.contrib.sites.shortcuts import get_current_site


def index(request):
    msg_count = ''
    if request.method == 'POST':
        captcha = False
        log_in(request,captcha) 
    if not request.user.is_authenticated():
        user = None
    else:
        user = request.user
        count = len(Message.objects.filter(receiver = user,readed = False))
        if count:
            msg_count = count
    return render(request,'index.html',{'user':user,'msg_count':msg_count})

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
            return HttpResponse('昵称或邮箱已存在')
        else:
            return redirect('accounts:login')
    else:
        return render(request,'accounts/register.html')

def log_in(request,captcha = True):
    user = None
    if request.method == 'POST':
        #return HttpResponse(form.)
        if captcha:
            form = CapchaFieldForm(request.POST)
            if form.is_valid():
                pass
            else:
                form = CapchaFieldForm()
                return HttpResponse("验证码错误!")
                return render(request,'accounts/login.html',{'form':form})
        email = request.POST['email']
    	password = request.POST['password']
    	user = authenticate(
        	username = email,
        	password = password,
            )
    	if user is not None:
            if user.is_active:
    	        login(request,user)

                try:
                    if request.POST['lng'] and request.POST['lat'] and request.POST['city']:
                        user.set_lng(request.POST['lng'])
                        user.set_lat(request.POST['lat'])
                        user.set_last_login_city(request.POST['city'])
                    if user.get_last_login_city() != request.POST['city']:
                        pass
                    else:
                        pass
                except Exception, e:
                    pass
                #should check if the location is changed
                user.set_online()
                user.save()
                return redirect('index')
    	    else:
    		    pass
    	else:
            form = CapchaFieldForm()
            return render(request,'accounts/login.html',{'error':'账户或密码错误','form':form})
    else:
        form = CapchaFieldForm()
        return render(request,'accounts/login.html',{'user':user,'form':form})

@login_required
def user_info(request,img=''):
    user = request.user
    if request.method == 'POST':
        if img == 'img':
            try:
                request.user.set_profile(request.FILES['profile'])
                request.user.save()
            except:
                pass
            return redirect('accounts:user_info')
        post = request.POST
        nn = post['nick_name']
        ht = post['height']
        wt = post['weight']
        ad = post['address']
        #em = post['email']
        wk = post['work']
        pn = post['phone_num']
        bd = post['birthday'].split('-')
        user.set_birthday(int(bd[0]),int(bd[1]),int(bd[2]))
        user.set_nick_name(nn)
        user.set_height(ht)
        user.set_weight(wt)
        user.set_address(ad)
        #user.set_email(em)
        user.set_work(wk)
        user.set_phone_num(pn)
        user.save()
        return redirect('accounts:user_info')
    else:
        context = {
                'sex':user.get_sex(),
                'real_name':user.get_real_name(),
                'nick_name':user.get_nick_name(),
                'email':user.get_email(),
                'work':user.get_work(),
                'birthday':user.get_birthday(),
                'phone_num':user.get_phone_num(),
                'weight':user.get_weight(),
                'height':user.get_height(),
                'age':user.get_age(),
                'address':user.get_address(),
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
    request.user.sam = ''
    request.user.save()
    logout(request)
    return redirect('index')

@login_required
def fri_list(request):
    fri_list = request.user.friends.all()
    return render(request,'accounts/friends.html',{'fri_list':fri_list})

@login_required
def fri_delete(request,user_id):
    request.user.del_friend(id = user_id)
    return redirect('accounts:fri_list')
@login_required
def fri_add(request,user_id):
    request.user.add_friend(user_id)
    obj = MyUser.objects.get(id = user_id)
    if request.user not in obj.friends.all():
        request.user.send_message(
            title = '好友请求',
            message = '你好，交个朋友吧',
            id = user_id,
            )
    return redirect('accounts:detail',user_id)

@login_required
def send(request,user_id):
    request.user.send_message(
        title = request.POST['title'],
        message = request.POST['message'],
        id = user_id,
        )
    return redirect('messages:index')
@login_required
def detail(request,user_id):
    obj = User.objects.get(id = user_id)
    user =request.user
    dist = 0.001*calc_dis(user.get_lng(),user.get_lat(),obj.get_lng(),obj.get_lat())
    if user in obj.friends.all():
        is_friend = True
    else:
        is_friend = False
    if is_friend and(obj in user.friends.all()):
        is_friend_each_other = True
    else:
        is_friend_each_other = False
    return render(request,'accounts/user_detail.html',{'obj':obj,'is_friend':is_friend,'is_friend_each_other':is_friend_each_other,'dist':dist})

def forget(request):
    return render(request,'accounts/forget_input_id.html')

def send_email(request):
    import sys
    reload(sys)   
    sys.setdefaultencoding('utf8')  
    current_site =  get_current_site(request)
    email = request.POST['email']
    encode = 'QAZWSXEDCRFVTGBYHNUJMIKOLPqazwsxedcrfvtgbyhnujmikolp0123456789'
    randomlength = 20;
    sam = sample(encode,randomlength)
    try:
        user = MyUser.objects.get(email = email)
        uid = user.id
        #return HttpResponse(uid)
    except MyUser.DoesNotExist as e:
        return HttpResponse('<h1>用户不存在</h1>')
    email_title = '拼游网更改密码'
    email_body = str('点击下面链接跳转:http://')+ str(current_site) + str('/accounts/changepasswd/')+ str(uid) + '/'+ ''.join(sam)
    send_status = send_mail(email_title,email_body,settings.EMAIL_HOST_USER,[email])
    user.sam = ''.join(sam) #turn list to string
    user.save()
    if send_status == 1: 
        return HttpResponse('<h1>请检查您的邮箱</h1>')
    else:
        return HttpResponse('<h1>发送错误,请重试</h1')

def change_passwd(request,user_id,sam):
    #return HttpResponse(sam+'  '+MyUser.objects.get(pk=user_id).sam )
    try:
        user = MyUser.objects.get(pk=user_id)
    except Exception as e:
        raise e
    else:
        if user.sam != sam:
            raise Http404()
    try:
        request.POST['password1']
    except Exception as e:
        return render(request,'accounts/change_passwd.html',{'uid':user_id})
    else:
        password = request.POST['password1']
        
        user.set_pswd(password)
        user.save()
        return redirect('accounts:login')
