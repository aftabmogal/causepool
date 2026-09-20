from django.contrib import admin
from .models import Score


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ["user", "value", "date"]
    list_filter = ["date"]
    search_fields = ["user__username"]
