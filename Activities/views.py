#coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from Activities.models import Activity
from django.http import HttpResponse
@login_required
def list(request):
    if request.method == 'POST':
        request.user.join_act(pk = int(request.POST['id']))
        return HttpResponse('ok')
    else:
        act_list = Activity.objects.get_valid_activity
        return render(request,'activities/index.html',{'act_list':act_list})

@login_required
def create(request):
    if request.method == 'POST':
        pass
    else:
        return render(request,'activities/create.html')

@login_required
def detail(request,activity_id):
    return render(request,'activities/detail.html')

