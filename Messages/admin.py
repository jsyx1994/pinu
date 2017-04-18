from django.contrib import admin

# Register your models here.
from Messages.models import Message

admin.site.register(Message)
