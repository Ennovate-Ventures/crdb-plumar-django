from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Watchlist, Contact, Project

# Register your models here.

admin.site.unregister(Group)
admin.site.site_header = 'Plumar Administration'

admin.site.register(Watchlist)
admin.site.register(Contact)
admin.site.register(Project)


