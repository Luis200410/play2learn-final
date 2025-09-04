from django.urls import path

from games.views import MathFactsView, AnagramHuntView, record_result, history_view, leaderboard_view, home_view, contact_view

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
    # History and leaderboards
    path('history/', history_view, name='history'),
    path('leaderboard/<slug:game_type>/', leaderboard_view, name='leaderboard'),
]
