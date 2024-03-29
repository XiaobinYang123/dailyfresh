# -*- coding: utf-8 -*-
from django.contrib import admin
from goods.models import GoodsType,Goods,GoodsSKU, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
from django.core.cache import cache
# Register your models here.


class BaseModelAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):

		super(BaseModelAdmin, self).save_model(request, obj, form, change)


		from celery_tasks.tasks import generate_static_index_html
		generate_static_index_html.delay()


		cache.delete('index_page_data')

	def delete_model(self, request, obj):

		super().delete_model(request, obj)

		from celery_tasks.tasks import generate_static_index_html
		generate_static_index_html.delay()


		cache.delete('index_page_data')


class GoodsTypeAdmin(BaseModelAdmin):
	pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
	pass


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
	pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
	pass


admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(GoodsSKU)

