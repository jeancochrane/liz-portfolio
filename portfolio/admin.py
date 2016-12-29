from django.contrib.admin import AdminSite

from .models import Category, Work, About


class LizAdmin(AdminSite):
    site_header = "Liz's portfolio administration"
    site_title = "Admin - Liz Barr"
    index_title = "Edit portfolio"


admin_site = LizAdmin()

admin_site.register(Category)
admin_site.register(Work)
admin_site.register(About)
