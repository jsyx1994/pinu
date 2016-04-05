#coding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils import timezone
class MessageManager(models.Manager):
    def create_message(self,title,message,sender,receiver):
        """
        create a message via title,message,sender and receiver
        """
        msg = super(MessageManager,self).create(
                title = title,
                message = message,
                sender = sender,
                receiver = receiver,
                )
        return msg

class Message(models.Model):
    title = models.CharField(
            max_length = 50,
            )

    message = models.CharField(
             max_length = 200,
             verbose_name = 'message content',
	    )

    sended_time = models.DateTimeField(
            default = timezone.now,
            )

    readed = models.BooleanField(
            default = False,
            )

    seder_preserved = models.BooleanField(
            default = True,
            )

    rcver_preserved = models.BooleanField(
            default = True,
            )

    sender = models.ForeignKey(
            settings.AUTH_USER_MODEL,
	    default = None,
	    related_name = 'sender',
	    )

    receiver = models.ForeignKey(
	    settings.AUTH_USER_MODEL,
	    default = None,
	    related_name = 'receiver',
	    )

    objects = MessageManager()
    def __unicode__(self):
	return self.title


    #set method
    def set_readed(self):
        self.readed = True

    def set_title(self,title):
        self.title = title

    def set_message(self,message):
        self.message = message

    #get method
    def get_title(self):
	return self.title

    def get_message(self):
        return self.message

    def get_sended_time(self):
	return self.sended_time

    @property
    def is_readed(self):
        """
        return value 'True' if the receiver has already read the message sent by the sender
        """
        return self.readed

    @property
    def is_sed_keep(self):
        return seder_preserved

    @property
    def is_rcv_keep(self):
        return rcver_preserved
