from django.urls import path

from games.views import MathFactsView, AnagramHuntView, record_result, history_view, leaderboard_view

app_name = 'games'
urlpatterns = [
    path('math-facts/', MathFactsView.as_view(), name='math-facts'),
    path('anagram-hunt/', AnagramHuntView.as_view(), name='anagram-hunt'),
    # API to record results
    path('api/games/results/', record_result, name='record-result'),
    # History and leaderboards
    path('history/', history_view, name='history'),
    path('leaderboard/<slug:game_type>/', leaderboard_view, name='leaderboard'),
]
