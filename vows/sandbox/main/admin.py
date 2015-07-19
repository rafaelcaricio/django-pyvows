from django.contrib import admin

from models import StringModel


class StringModelAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(StringModel, StringModelAdmin)
