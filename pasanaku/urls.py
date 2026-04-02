from django.urls import path

from .views import configure_pasanaku

urlpatterns = [
    path('<int:pasanaku_id>/configure/', configure_pasanaku, name='configure_pasanaku'),
]
