#coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from Activities.models import Activity

@login_required
def list(request):
    act_list = Activity.objects.get_valid_activity
    return render(request,'activities/list.html',{'act_list':act_list})

@login_required
def create(request):
    pass

@login_required
def detail(request,activity_id):
    return render(request,'activities/detail.html')

