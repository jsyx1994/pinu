#coding:utf-8
from django.shortcuts import render,HttpResponse,redirect
from django.utils import timezone
from .forms import PostForm
from .models import Diary
from Activities.models import Activity
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
	diaries = Diary.objects.filter(public = True).order_by('-finished_time') #if the diary is public,find it and show it
	return render(request,'diaries/index.html',{'diaries':diaries})

@login_required
def edit(request,act_id):
	act = Activity.objects.get(pk=act_id)
	act_title = act.get_title()
	if request.method == 'POST':
		form =PostForm(request.POST)
		if form.is_valid():
			auth = request.user
			content = form.cleaned_data['content']
			title = form.cleaned_data['title']
			finished_time = timezone.now()
			diary = Diary(
				author = auth,
				act_belonged = act,
				title = title,
				finished_time = finished_time,
				content = content,
				)
			diary.save()
			return redirect('diaries:myself')
	else:
		form = PostForm()
	return render(request,'diaries/edit.html',{'form':form,'act_title':act_title})

@login_required
def myself(request):
	diaries = Diary.objects.filter(author=request.user).order_by('-finished_time')
	return render(request,'diaries/myself.html',{'diaries':diaries})


def detail(request,dia_id):
	try:
		diary = Diary.objects.get(pk = dia_id)
	except Diary.DoesNotExist as e:
		raise e

	content = diary.get_content()
	#return HttpResponse(content)
	title = diary.get_title()
	finished_time = diary.get_finished_time()
	author =diary.author.get_nick_name()
	return render(request,'diaries/detail.html',{'title':title,'content':content,'finished_time':finished_time,'author':author})

@login_required
def alter(request,dia_id):
	diary = Diary.objects.get(pk = dia_id)
	act = diary.act_belonged

	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():	
			diary.title = form.cleaned_data['title']
			diary.content = form.cleaned_data['content']
			diary.finished_time = timezone.now()
			diary.save()
			return redirect('diaries:myself')

	act_id = act.id
	act_title = act.get_title
	title = diary.get_title()
	content = diary.get_content()
	public = diary.public
	data = {'title':title,
			'content':content,
			'public':public,
			}
	form = PostForm(data)
	return render(request,'diaries/alter.html',{'form':form,'act_title':act_title,'dia_id':dia_id})