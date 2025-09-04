import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView

from .models import GameResult


class MathFactsView(TemplateView):
    template_name = "math-facts.html"


class AnagramHuntView(TemplateView):
    template_name = "anagram-hunt.html"


@require_POST
@csrf_protect
def record_result(request):
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else request.POST
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    game_type = data.get("game_type")
    score = data.get("score")
    settings = data.get("settings", {})

    if game_type not in dict(GameResult.GameType.choices):
        return HttpResponseBadRequest("Invalid game_type")
    try:
        score = int(score)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid score")

    result = GameResult.objects.create(
        user=request.user if request.user.is_authenticated else None,
        game_type=game_type,
        score=score,
        settings=settings,
    )
    return JsonResponse({
        "ok": True,
        "id": result.id,
        "finished_at": result.finished_at.isoformat(),
    })


@login_required
def history_view(request):
    results = GameResult.objects.filter(user=request.user)
    return render(request, "games/history.html", {"results": results})


def leaderboard_view(request, game_type):
    if game_type not in dict(GameResult.GameType.choices):
        return HttpResponseBadRequest("Invalid game_type")
    results = GameResult.objects.filter(game_type=game_type).select_related("user").order_by("-score", "finished_at")[:100]
    return render(request, "games/leaderboard.html", {
        "results": results,
        "game_type": game_type,
        "game_type_label": dict(GameResult.GameType.choices)[game_type],
    })
