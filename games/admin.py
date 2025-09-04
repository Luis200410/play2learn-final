from django.contrib import admin
from .models import GameResult


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ("finished_at", "user", "game_type", "score")
    list_filter = ("game_type", "finished_at")
    search_fields = ("user__username",)

# Register your models here.
