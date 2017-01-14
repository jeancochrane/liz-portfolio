from django.contrib.admin import AdminSite
from django.contrib import admin

from .models import Category, Work, About, Contact, Project


class LizAdmin(AdminSite):
    site_header = "Liz's portfolio administration"
    site_title = "Admin - Liz Barr"
    index_title = "Edit portfolio"


class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    list_filter = ('project', 'featured')

admin_site = LizAdmin()

admin_site.register(Category)
admin_site.register(Work, WorkAdmin)
admin_site.register(Project)
admin_site.register(About)
admin_site.register(Contact)
