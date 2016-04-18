#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Message
@login_required
def list(request):
    msg_list = Message.objects.filter(receiver = request.user).order_by('-sended_time')
    return render(request,'messages/index.html',{'msg_list':msg_list})

@login_required
def detail(request):
    pass
