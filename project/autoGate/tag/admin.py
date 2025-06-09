from django.contrib import admin

# Register your models here.

from .models import Tag, TagPermission



admin.site.register(Tag)
admin.site.register(TagPermission)
