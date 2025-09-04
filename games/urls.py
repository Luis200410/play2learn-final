from django.urls import path

from games.views import (
    MathFactsView,
    AnagramHuntView,
    record_result,
    history_view,
    leaderboard_view,
    home_view,
    contact_view,
    history_api,
    leaderboard_api,
)

app_name = 'games'
urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact_view, name='contact'),
    # Game pages: support both with and without trailing slash
    path('math-facts', MathFactsView.as_view(), name='math-facts'),
    path('math-facts/', MathFactsView.as_view(), name='math-facts-slash'),
    path('anagram-hunt', AnagramHuntView.as_view(), name='anagram-hunt'),
    path('anagram-hunt/', AnagramHuntView.as_view(), name='anagram-hunt-slash'),
    # API to record results
    path('api/games/results/', record_result, name='record-result'),
    # JSON APIs for in-page tables
    path('api/games/history/<slug:game_type>/', history_api, name='history-api'),
    path('api/games/leaderboard/<slug:game_type>/', leaderboard_api, name='leaderboard-api'),
    # History and leaderboards
    path('history/', history_view, name='history'),
    path('leaderboard/<slug:game_type>/', leaderboard_view, name='leaderboard'),
]
