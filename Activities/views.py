#coding:utf-8
from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from Activities.models import Activity
from django.http import HttpResponse
from datetime import datetime
import operator
@login_required
def list(request,option = 'default'):
    act_list = act_list = Activity.objects.get_valid_activity()
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
        if request.method == 'GET':
            if option == 'bytime':
                bytime = operator.attrgetter('pub_time')
                act_list = sorted(act_list,key = bytime,reverse = True)
                return render(request,'activities/index.html',{'act_list':act_list})
            if option == 'nearme':
                user = request.user
                act_list = user.nearby_act()
                return render(request,'activities/index.html',{'act_list':act_list})
            else:
                return render(request,'activities/index.html',{'act_list':act_list})

@login_required
def create(request):
    if request.method == 'POST':
        post = request.POST
        x,y= post['start_time'].split(' ') , post['end_time'].split(' ')
        x0,y0 = x[0],y[0]
        x1,y1 = x[1],y[1]
        st1 = x0.split('-')
        st2 = x1.split(':')
        ed1 = y0.split('-')
        ed2 = y1.split(':')
        st = datetime(int(st1[0]),int(st1[1]),int(st1[2]),int(st2[0]),int(st2[1]))
        ed = datetime(int(ed1[0]),int(ed1[1]),int(ed1[2]),int(ed2[0]),int(ed2[1]))
        act = Activity.objects.create_activity(
            title = post['title'],
            category = (post['category'][:2]).upper(),
            person_num_limit = int(post['person_limit']),
            start_time = st,
            due_time = ed,
            advocator = request.user,
            )
        act.set_slng(post['slng'])
        act.set_slat(post['slat'])
        act.set_dlng(post['dlng'])
        act.set_dlat(post['dlat'])
        act.set_st_place(post['starting_place'])
        act.set_ds_place(post['destination'])
        act.save()
        return HttpResponse(post['start_time'])
    else:
        return render(request,'activities/create.html')

@login_required
def detail(request,activity_id):
    return render(request,'activities/detail.html')

@login_required
def myself(request):
    joined_list = Activity.objects.filter(person_joined=request.user)
    return render(request,'activities/myself.html',{'joined_list':joined_list})