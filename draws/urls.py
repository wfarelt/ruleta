from django.urls import path
from .views import execute_draw, roulette_view, draw_history, reset_draw, save_rotation_angle

urlpatterns = [
    path('roulette/<int:pasanaku_id>/', roulette_view, name='roulette'),
    path('execute/<int:pasanaku_id>/', execute_draw, name='execute_draw'),
    path('history/<int:pasanaku_id>/', draw_history, name='draw_history'),
    path('reset/<int:pasanaku_id>/', reset_draw, name='reset_draw'),
    path('save_angle/<int:pasanaku_id>/', save_rotation_angle, name='save_rotation_angle'),
]