from django.urls import path
from .views import dashboard

urlpatterns = [
    path('', dashboard, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
]
