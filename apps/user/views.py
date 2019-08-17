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

	    # 进行数据校验
		if not all([username, password, email]):
	        # 数据不完整
			return render(request, 'register.html', {'errmsg':'数据不完整'})

	    # 校验邮箱
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
	        # 用户名已存在
			return render(request, 'register.html', {'errmsg':'用户名已存在'})

	    # 进行业务处理: 进行用户注册
		user = User.objects.create_user(username, email, password)
		user.is_active = 0
		print(username)
		print(email)
		print(password)
		user.save()

	    # 返回应答, 跳转到首页
		return redirect(reverse('goods:index'))


class RegisterView(View):
	def get(self, request):
		return render(request, 'register.html')

	def post(self, request):
		username = request.POST.get('user_name')
		password = request.POST.get('pwd')
		email = request.POST.get('email')
		allow = request.POST.get('allow')

	    # 进行数据校验
		if not all([username, password, email]):
	        # 数据不完整
			return render(request, 'register.html', {'errmsg':'数据不完整'})

	    # 校验邮箱
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
	        # 用户名已存在
			return render(request, 'register.html', {'errmsg':'用户名已存在'})

	    # 进行业务处理: 进行用户注册
		user = User.objects.create_user(username, email, password)
		user.is_active = 0
		user.save()

		serializer=Serializer(settings.SECRET_KEY, 3600)
		info={'confirm':user.id}
		token=serializer.dumps(info)  #bytes
		token=token.decode()

		#放任务队列
		send_register_active_email.delay(email, username, token)  
	    # 返回应答, 跳转到首页
		return redirect(reverse('goods:index'))

#网易授权密码 admin123
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
		    # 用户名密码正确
		    if user.is_active:
		        # 用户已激活
		        # 记录用户的登录状态
		        login(request, user)

		        # 获取登录后所要跳转到的地址
		        # 默认跳转到首页
		        # 拿不到next就到index
		        next_url = request.GET.get('next', reverse('goods:index'))

		        # 跳转到next_url
		        response = redirect(next_url) # HttpResponseRedirect

		        # 判断是否需要记住用户名
		        remember = request.POST.get('remember')

		        if remember == 'on':
		            # 记住用户名
		            response.set_cookie('username', username, max_age=7*24*3600)
		        else:
		            response.delete_cookie('username')

		        # 返回response
		        return response
		    else:
		        # 用户未激活
		        return render(request, 'login.html', {'errmsg':'账户未激活'})
		else:
		    # 用户名或密码错误
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

		history_key='htistory_%d'%user.id
		sku_ids=con.lrange(history_key, 0, 4)

		goods_li = []
		for id in sku_ids:
			goods = GoodsSKU.objects.get(id=id)
			goods_li.append(goods)

		# 组织上下文
		context = {'page':'user','address':address,'goods_li':goods_li}

		# 除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件
		return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'user_center_order.html', {'page':'order'})

class UserAddressView(LoginRequiredMixin, View):
	def get(self, request):
	# 获取登录用户对应User对象
		user = request.user

		# 获取用户的默认收货地址
		address = Address.objects.get_default_address(user)
		# address = Address.objects.get_default_address(user)

		# 使用模板
		return render(request, 'user_center_site.html', {'page':'address', 'address':address})

	def post(self, request):
		receiver = request.POST.get('receiver')
		addr = request.POST.get('addr')
		zip_code = request.POST.get('zip_code')
		phone = request.POST.get('phone')

		# 校验数据
		if not all([receiver, addr, phone, type]):
		    return render(request, 'user_center_site.html', {'errmsg':'数据不完整'})

		# 校验手机号
		if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
		    return render(request, 'user_center_site.html', {'errmsg':'手机格式不正确'})

		# 业务处理：地址添加
		# 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
		# 获取登录用户对应User对象
		user = request.user

		# try:
		#     address = Address.objects.get(user=user, is_default=True)
		# except Address.DoesNotExist:
		#     # 不存在默认收货地址
		#     address = None

		address = Address.objects.get_default_address(user)

		if address:
		    is_default = False
		else:
		    is_default = True

		# 添加地址
		Address.objects.create(user=user,
		                       receiver=receiver,
		                       addr=addr,
		                       zip_code=zip_code,
		                       phone=phone,
		                       is_default=is_default)

		# 返回应答,刷新地址页面
		return redirect(reverse('user:address')) # get请求方式