from django.contrib import admin
from .models import Pasanaku, Participation


@admin.register(Pasanaku)
class PasanakuAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'start_date',
        'total_participants',
        'monthly_amount',
        'draws_per_month',
        'status'
    )

    list_filter = ('status', 'start_date')
    search_fields = ('name',)
    
@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'pasanaku', 'is_winner', 'winning_position')
    list_filter = ('is_winner', 'pasanaku')
    search_fields = ('participant__full_name',)
