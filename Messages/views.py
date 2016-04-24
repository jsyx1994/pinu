#coding:utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Message
@login_required
def list(request,option=''):
	can_reply = True
	msg_list = Message.objects.filter(receiver = request.user).order_by('-sended_time')
	if option == 'unreaded':
		msg_list = msg_list.filter(readed = False)
	if option == 'rcver':
		msg_list = msg_list.filter(rcver_preserved = True)
	if option == 'sender':
		msg_list = Message.objects.filter(sender = request.user).filter(seder_preserved = True).order_by('-sended_time')
		can_reply = False
	if option == 'trash':
		pass
	return render(request,'messages/index.html',{'msg_list':msg_list,'can_reply':can_reply})

@login_required
def detail(request):
    pass

@login_required
def delete(request,msg_id):
	msg = Message.objects.get(id = msg_id)
	msg.rcver_preserved = False
	msg.save()
	return redirect('messages:index')