from django.contrib import admin
from .models import Pasanaku, Participation


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1
    fields = ('participant', 'is_winner', 'is_temporarily_removed', 'winning_position')
    readonly_fields = ('is_winner', 'winning_position')
    raw_id_fields = ('participant',)


@admin.register(Pasanaku)
class PasanakuAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'start_date',
        'total_participants',
        'monthly_amount',
        'draws_per_month',
        'draws_before_winner',
        'status'
    )

    list_filter = ('status', 'start_date')
    search_fields = ('name',)
    inlines = [ParticipationInline]
    
@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'pasanaku', 'is_winner', 'is_temporarily_removed', 'winning_position')
    list_filter = ('is_winner', 'is_temporarily_removed', 'pasanaku')
    search_fields = ('participant__full_name',)
