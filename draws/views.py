from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from pasanaku.models import Pasanaku, Participation
from .services import perform_draw

def execute_draw(request, pasanaku_id):

    pasanaku = get_object_or_404(Pasanaku, id=pasanaku_id)

    winner = perform_draw(pasanaku)

    if winner:
        messages.success(
            request,
            f"Winner: {winner.participant.full_name}"
        )
    else:
        messages.warning(
            request,
            "No more participants available for draw."
        )

    return redirect('admin:pasanaku_pasanaku_changelist')


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