# -*- coding:UTF-8 -*-
from django.conf.urls import url
from user import views
from django.contrib.auth.decorators import login_required
from user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserAddressView, UserOrderView, LogoutView

urlpatterns = [
	# url(r'^register$', views.register, name='register'),
	# url(r'^register_handle$', views.register_handle, name='register_handle'),
	url(r'^register$', RegisterView.as_view(), name='register'),
	url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),

	url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'), # 注销登录

	url(r'^$', UserInfoView.as_view(), name='user'),
	url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),
	url(r'^address$', UserAddressView.as_view(), name='address'),
]


    # url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'), # 