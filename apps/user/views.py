# -*- coding:UTF-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.views.generic import View
from django.http import HttpResponse
from user.models import User, Address
from goods.models import GoodsSKU
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

from order.models import OrderInfo, OrderGoods
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from celery_tasks.tasks import send_register_active_email
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
import re

# Create your views here.
def register(request):
	if request.method== 'Get':
		return render(request, 'register.html')
	else:
		username = request.POST.get('user_name')
		password = request.POST.get('pwd')
		email = request.POST.get('email')
		allow = request.POST.get('allow')


		if not all([username, password, email]):

			return render(request, 'register.html', {'errmsg':'数据不完整'})


		if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
			return render(request, 'register.html', {'errmsg':'邮箱格式不正确'})

		if allow != 'on':
			return render(request, 'register.html', {'errmsg':'请同意协议'})

		try:
			user = User.objects.get(username=username)  #查不到抛异常
		except User.DoesNotExist:

			user = None

		if user:

			return render(request, 'register.html', {'errmsg':'用户名已存在'})


		user = User.objects.create_user(username, email, password)
		user.is_active = 0
		print(username)
		print(email)
		print(password)
		user.save()


		return redirect(reverse('goods:index'))


class RegisterView(View):
	def get(self, request):
		return render(request, 'register.html')

	def post(self, request):
		username = request.POST.get('user_name')
		password = request.POST.get('pwd')
		email = request.POST.get('email')
		allow = request.POST.get('allow')


		if not all([username, password, email]):

			return render(request, 'register.html', {'errmsg':'数据不完整'})


		if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
			return render(request, 'register.html', {'errmsg':'邮箱格式不正确'})

		if allow != 'on':
			return render(request, 'register.html', {'errmsg':'请同意协议'})

		try:
			user = User.objects.get(username=username)  #查不到抛异常
		except User.DoesNotExist:
	        # 用户名不存在
			user = None

		if user:

			return render(request, 'register.html', {'errmsg':'用户名已存在'})

		user = User.objects.create_user(username, email, password)
		user.is_active = 0
		user.save()

		serializer=Serializer(settings.SECRET_KEY, 3600)
		info={'confirm':user.id}
		token=serializer.dumps(info)  #bytes
		token=token.decode()

		send_register_active_email.delay(email, username, token)  

		return redirect(reverse('goods:index'))


class ActiveView(View):
	def get(self, request, token):
		#解密
		serializer=Serializer(settings.SECRET_KEY, 3600)
		
		try:
			info=serializer.loads(token)
			user_id=info['confirm']
			user=User.objects.get(id=user_id)
			user.is_active=1
			user.save()

			return redirect(reverse('user:login'))

		except SignatureExpired as e:
			return HttpResponse('激活链接过期')


class LoginView(View):
	def get(self, request):

		if 'username' in request.COOKIES:
			username=request.COOKIES.get('username')
			checked='checked'
			print(username)
			print(checked)
		else:
			username=''
			checked=''

		return render(request, 'login.html', {'username':username, 'checked':checked})

	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('pwd')

        # 校验数据
		if not all([username, password]):
		    return render(request, 'login.html', {'errmsg':'数据不完整'})

		# 业务处理:登录校验
		user = authenticate(username=username, password=password)

		if user is not None:

		    if user.is_active:

		        login(request, user)


		        next_url = request.GET.get('next', reverse('goods:index'))


		        response = redirect(next_url) # HttpResponseRedirect


		        remember = request.POST.get('remember')

		        if remember == 'on':

		            response.set_cookie('username', username, max_age=7*24*3600)
		        else:
		            response.delete_cookie('username')


		        return response
		    else:

		        return render(request, 'login.html', {'errmsg':'账户未激活'})
		else:

		    return render(request, 'login.html', {'errmsg':'用户名或密码错误'})


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect(reverse('goods:index'))


class UserInfoView(LoginRequiredMixin, View):
	def get(self, request):
		user = request.user
		address = Address.objects.get_default_address(user)                    #直接把user给模板了

		con=get_redis_connection('default')

		history_key='history_%d'%user.id
		sku_ids=con.lrange(history_key, 0, 4)

		goods_li = []
		for id in sku_ids:
			goods = GoodsSKU.objects.get(id=id)
			goods_li.append(goods)


		context = {'page':'user','address':address,'goods_li':goods_li}


		return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):

	def get(self, request, page):

		user = request.user
		orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

		for order in orders:

			order_skus = OrderGoods.objects.filter(order_id=order.order_id)


			for order_sku in order_skus:

				amount = order_sku.count*order_sku.price

				order_sku.amount = amount

			order.status_name = OrderInfo.ORDER_STATUS[order.order_status]

			order.order_skus = order_skus

		# 分页
		paginator = Paginator(orders, 1)


		try:
			page = int(page)
		except Exception as e:
			page = 1

		if page > paginator.num_pages:
			page = 1


		order_page = paginator.page(page)


		num_pages = paginator.num_pages
		if num_pages < 5:
			pages = range(1, num_pages + 1)
		elif page <= 3:
			pages = range(1, 6)
		elif num_pages - page <= 2:
			pages = range(num_pages - 4, num_pages + 1)
		else:
			pages = range(page - 2, page + 3)


		context = {'order_page':order_page,
		'pages':pages,
		'page': 'order'}

		# 使用模板
		return render(request, 'user_center_order.html', context)

class UserAddressView(LoginRequiredMixin, View):
	def get(self, request):

		user = request.user


		address = Address.objects.get_default_address(user)



		return render(request, 'user_center_site.html', {'page':'address', 'address':address})

	def post(self, request):
		receiver = request.POST.get('receiver')
		addr = request.POST.get('addr')
		zip_code = request.POST.get('zip_code')
		phone = request.POST.get('phone')


		if not all([receiver, addr, phone, type]):
		    return render(request, 'user_center_site.html', {'errmsg':'数据不完整'})

		# 校验手机号
		if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
		    return render(request, 'user_center_site.html', {'errmsg':'手机格式不正确'})


		user = request.user



		address = Address.objects.get_default_address(user)

		if address:
		    is_default = False
		else:
		    is_default = True

		Address.objects.create(user=user,
		                       receiver=receiver,
		                       addr=addr,
		                       zip_code=zip_code,
		                       phone=phone,
		                       is_default=is_default)


		return redirect(reverse('user:address')) 