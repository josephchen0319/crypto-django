from django.contrib import admin
from .models import Filter


class FilterAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Filter, FilterAdmin)
