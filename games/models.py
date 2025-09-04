from django.db import models
from django.contrib.auth import get_user_model


class GameResult(models.Model):
    class GameType(models.TextChoices):
        MATH_FACTS = "math_facts", "Math Facts Practice"
        ANAGRAM_HUNT = "anagram_hunt", "Anagram Hunt"

    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name="game_results")
    game_type = models.CharField(max_length=32, choices=GameType.choices)
    settings = models.JSONField(default=dict, blank=True)
    score = models.IntegerField()
    finished_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-finished_at"]

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.get_game_type_display()} - {self.score}"

# Create your models here.
