import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView

from .models import GameResult, Review
from .forms import ReviewForm, ContactForm


class MathFactsView(TemplateView):
    template_name = "math-facts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Leaderboard for all users
        context["leaderboard"] = (
            GameResult.objects.filter(game_type=GameResult.GameType.MATH_FACTS)
            .select_related("user")
            .order_by("-score", "finished_at")[:20]
        )
        # Per-user history
        if self.request.user.is_authenticated:
            context["history"] = (
                GameResult.objects.filter(user=self.request.user, game_type=GameResult.GameType.MATH_FACTS)
                .order_by("-finished_at")[:50]
            )
        else:
            context["history"] = []
        return context


class AnagramHuntView(TemplateView):
    template_name = "anagram-hunt.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Leaderboard for all users
        context["leaderboard"] = (
            GameResult.objects.filter(game_type=GameResult.GameType.ANAGRAM_HUNT)
            .select_related("user")
            .order_by("-score", "finished_at")[:20]
        )
        # Per-user history
        if self.request.user.is_authenticated:
            context["history"] = (
                GameResult.objects.filter(user=self.request.user, game_type=GameResult.GameType.ANAGRAM_HUNT)
                .order_by("-finished_at")[:50]
            )
        else:
            context["history"] = []
        return context


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


def home_view(request):
    # Prefer featured reviews if any exist; else fall back to all reviews
    featured = Review.objects.filter(featured=True)[:10]
    reviews = featured if featured.exists() else Review.objects.all()[:10]

    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                Review.objects.create(user=request.user, content=form.cleaned_data["content"])
                return redirect("games:home")
        else:
            form = ReviewForm()

    return render(request, "home.html", {
        "reviews": reviews,
        "form": form,
    })


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            subject = f"Play2Learn Contact: {name}"
            body = f"From: {name} <{email}>\n\n{message}"

            # Send to all superusers with an email address
            from django.contrib.auth import get_user_model
            User = get_user_model()
            recipients = list(User.objects.filter(is_superuser=True).exclude(email="").values_list("email", flat=True))
            if not recipients:
                recipients = [email]  # fallback: send back to sender in dev

            send_mail(subject, body, None, recipients)
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect("games:contact")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
