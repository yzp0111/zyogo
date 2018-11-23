from django.contrib import admin
from .models import *
# Register your models here.
#tarena:zhangsanfeng
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'uphone','isCustomer','isBusiness','isActive')
    list_display_links = ('username', 'uphone')

class GoodsInfoAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    search_fields = ('goods_name',)

class WindowsAdmin(admin.ModelAdmin):
    list_display = ('store', 'windows_id','goods','staring_date','end_date')
    list_filter = ('store',)

class ShoppingRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_number','goods_name','ispay')
    list_filter = ('user',)
    search_fields = ('user','order_number')
#用户基础信息表
admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)
admin.site.register(Store)
admin.site.register(Windows,WindowsAdmin)
admin.site.register(ShoppingRecord,ShoppingRecordAdmin)

