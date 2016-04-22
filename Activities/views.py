#coding:utf-8
from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from Activities.models import Activity
from django.http import HttpResponse
from datetime import datetime
from Accounts.haversine import calc_dis
import operator
@login_required
def list(request,option = 'default'):
    #cannot join if have conflict time between two:pass 
    if request.method == 'POST':
        act_id = int(request.POST['act_id'])
        if request.user.join_act(pk = act_id):
            #add all the followers in the activity you joined to your friend list,vs
            ps_list = Activity.objects.get(pk=act_id).person_joined.all()
            for i in ps_list:
                if i!=request.user:
                    request.user.add_friend(id = i.id)
                    i.add_friend(id = request.user.id)
            return redirect('activities:myself')
        else:
            act_list = Activity.objects.get_valid_activity()
            dist_list = map(lambda x:0.001*calc_dis(request.user.get_lng(),request.user.get_lat(),x.get_slng(),x.get_slat()),act_list)
            return render(request,'activities/index.html',{'error':'cannot join:conflict','act_list':act_list})
    if request.method == 'GET':
        if option == 'bytime':
            bytime = operator.attrgetter('pub_time')
            act_list = Activity.objects.get_valid_activity()
            act_list = sorted(act_list,key = bytime,reverse = True)
            dist_list = map(lambda x:0.001*calc_dis(request.user.get_lng(),request.user.get_lat(),x.get_slng(),x.get_slat()),act_list)
            return render(request,'activities/index.html',{'act_list':act_list,'dist_list':dist_list})
        if option == 'nearme':
            user = request.user
            act_list = user.nearby_act()
            dist_list = map(lambda x:0.001*calc_dis(user.get_lng(),user.get_lat(),x.get_slng(),x.get_slat()),act_list)
            return render(request,'activities/index.html',{'act_list':act_list,'dist_list':dist_list})
        else:
            act_list = Activity.objects.get_valid_activity()
            dist_list = map(lambda x:0.001*calc_dis(request.user.get_lng(),request.user.get_lat(),x.get_slng(),x.get_slat()),act_list)
            return render(request,'activities/index.html',{'act_list':act_list,'dist_list':dist_list})

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