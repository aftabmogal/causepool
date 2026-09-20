from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
admin.site.site_header = "Digital Heroes Admin"
admin.site.site_title = "Digital Heroes Admin"
admin.site.index_title = "Platform Control Center"
