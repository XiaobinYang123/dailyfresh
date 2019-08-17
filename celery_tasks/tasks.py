# -*- coding:UTF-8 -*-
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time

#初始化， 在任务处理者
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()

app=Celery('celert_tasks.tasks', broker='redis://127.0.0.1:6379/8')

@app.task
def send_register_active_email(to_email, username, token):
	#发邮件
	subject='daily fresh'
	message=''
	sender=settings.EMAIL_FROM
	receiver=[to_email]
	html_message='<h1>天天生鲜项目, %s, 欢迎你<h1>请点击下列链接激活账号<br><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username, token, token)
	send_mail(subject, message, sender, receiver, html_message=html_message )  #阻塞执行