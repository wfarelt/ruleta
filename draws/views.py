from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from pasanaku.models import Pasanaku, Participation
from .models import Draw
from .services import perform_draw
from participants.models import Participant
from django.db.models import Count


def execute_draw(request, pasanaku_id):

    pasanaku = get_object_or_404(Pasanaku, id=pasanaku_id)

    winner = perform_draw(pasanaku)

    if not winner:
        return JsonResponse({
            "success": False,
            "message": "No participants available."
        })

    return JsonResponse({
        "success": True,
        "winner_id": winner.id,
        "winner_name": winner.participant.full_name,
        "position": winner.winning_position
    })


def roulette_view(request, pasanaku_id):
    pasanaku = get_object_or_404(Pasanaku, id=pasanaku_id)

    participants = Participation.objects.filter(
        pasanaku=pasanaku,
        is_winner=False
    )

    return render(request, 'draws/roulette.html', {
        'pasanaku': pasanaku,
        'participants': participants
    })


def draw_history(request, pasanaku_id):
    pasanaku = get_object_or_404(Pasanaku, id=pasanaku_id)

    winners = Participation.objects.filter(
        pasanaku=pasanaku,
        is_winner=True
    ).order_by('winning_position')

    return render(request, 'draws/draw_history.html', {
        'pasanaku': pasanaku,
        'winners': winners
    })


def dashboard(request):
    total_pasanakus = Pasanaku.objects.count()
    total_participants = Participant.objects.count()
    total_draws = Draw.objects.count()

    recent_draws = Draw.objects.select_related(
        'pasanaku', 'participation__participant'
    ).order_by('-draw_date')[:5]

    recent_winners = Participation.objects.filter(
        is_winner=True
    ).select_related('participant', 'pasanaku').order_by('-created_at')[:5]

    # top pasanakus by number of participants
    pasanakus_participants = Pasanaku.objects.annotate(
        participants_count=Count('participations')
    ).order_by('-participants_count')[:5]

    return render(request, 'draws/dashboard.html', {
        'total_pasanakus': total_pasanakus,
        'total_participants': total_participants,
        'total_draws': total_draws,
        'recent_draws': recent_draws,
        'recent_winners': recent_winners,
        'pasanakus_participants': pasanakus_participants,
    })
