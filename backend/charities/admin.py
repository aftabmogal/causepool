from django.contrib import admin
from .models import Charity, CharityEvent


class CharityEventInline(admin.TabularInline):
    model = CharityEvent
    extra = 1


@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ["name", "is_featured", "is_active", "created_at"]
    list_filter = ["is_featured", "is_active"]
    search_fields = ["name"]
    inlines = [CharityEventInline]
