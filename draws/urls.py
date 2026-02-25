from django.urls import path
from .views import execute_draw, roulette_view, draw_history

urlpatterns = [
    path('roulette/<int:pasanaku_id>/', roulette_view, name='roulette'),
    path('execute/<int:pasanaku_id>/', execute_draw, name='execute_draw'),
    path('history/<int:pasanaku_id>/', draw_history, name='draw_history'),
]