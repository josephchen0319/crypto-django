from django.contrib import admin
from member.models import Member, Notification, Following, SavedFilterGroup, FilterDetail
# Register your models here.
admin.site.register(Member)
admin.site.register(Notification)
admin.site.register(Following)
admin.site.register(SavedFilterGroup)
admin.site.register(FilterDetail)
