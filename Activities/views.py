#coding:utf-8
from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from Activities.models import Activity
from django.http import HttpResponse

@login_required
def list(request):
    if request.method == 'POST':
        #cannot join if have conflict time between two:pass  
        act_id = int(request.POST['act_id'])
        request.user.join_act(pk = act_id)
        #add all the followers in the activity you joined to your friend list
        ps_list = Activity.objects.get(pk=act_id).person_joined.all()
        for i in ps_list:
            if i!=request.user:
                request.user.add_friend(nick_name = i.nick_name)
        return redirect('activities:myself')
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

@login_required
def myself(request):
    return HttpResponse('this works')