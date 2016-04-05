from django.shortcuts import render

# Create your views here.

def list(request):
    pass

def create(request):
    pass

def detail(request,activity_id):
    return render(request,'activities/detail.html')

