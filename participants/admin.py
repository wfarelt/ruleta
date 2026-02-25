from django.contrib import admin
from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('full_name', 'phone', 'email')
