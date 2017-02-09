from django.contrib.admin import AdminSite
from django.contrib import admin
from django import forms

from .models import Category, About, Project, Contact, Work, Exhibitions


class ProjectForm(forms.ModelForm):
    class Meta(object):
        model = Project
        fields = "__all__"
        widgets = {
            'slug': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm


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
admin_site.register(Project, ProjectAdmin)
admin_site.register(About)
admin_site.register(Contact)
admin_site.register(Exhibitions)
admin_site.register(Work, WorkAdmin)
