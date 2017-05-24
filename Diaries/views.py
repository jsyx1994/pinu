#coding:utf-8
from django.shortcuts import render,HttpResponse
from django.utils import timezone
from .forms import PostForm
from .models import Diary
from Activities.models import Activity
# Create your views here.

def index(request):
	form = PostForm();
	return render(request,'diaries/index.html',{'form':form})

def edit(request,act_id):
	act_title = Activity.objects.get(pk=act_id)
	if request.method == 'POST':
		form =PostForm(request.POST)
		if form.is_valid():
			auth = request.user
			content = form.cleaned_data['content']
			title = form.cleaned_data['title']
			finished_time = timezone.now()
			diary = Diary(
				author = auth,
				title = title,
				finished_time = finished_time,
				content = content,
				)
			diary.save()
			return HttpResponse(finished_time)
	else:
		form = PostForm()
	return render(request,'diaries/edit.html',{'form':form,'act_title':act_title})
