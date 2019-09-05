# -*- coding:UTF-8 -*-

from django.core.mail import send_mail
from django.conf import settings
from django.template import loader, RequestContext
from celery import Celery
import time

#初始化， 在任务处理者
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()


from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django_redis import get_redis_connection


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


@app.task
def generate_static_index_html():

	types = GoodsType.objects.all()

	goods_banners = IndexGoodsBanner.objects.all().order_by('index')

	promotion_banners = IndexPromotionBanner.objects.all().order_by('index')


	for type in types:  # GoodsType

		image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')

		title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')


		type.image_banners = image_banners
		type.title_banners = title_banners



	context = {'types': types,
		'goods_banners': goods_banners,
		'promotion_banners': promotion_banners}


	temp = loader.get_template('static_index.html')

	static_index_html = temp.render(context)


	save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
	with open(save_path, 'w') as f:
		f.write(static_index_html)