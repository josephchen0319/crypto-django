from django.contrib import admin
from member.models import Member, Notification, Following, Saved_filter_group, Filter_group_detail
# Register your models here.
admin.site.register(Member)
admin.site.register(Notification)
admin.site.register(Following)
admin.site.register(Saved_filter_group)
admin.site.register(Filter_group_detail)
