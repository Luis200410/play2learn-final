from django.contrib import admin
from .models import GameResult, Review


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ("finished_at", "user", "game_type", "score")
    list_filter = ("game_type", "finished_at")
    search_fields = ("user__username",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "featured")
    list_filter = ("featured", "created_at")
    search_fields = ("user__username", "content")

# Register your models here.
