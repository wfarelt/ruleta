import random
from django.db import transaction
from pasanaku.models import Participation
from .models import Draw


@transaction.atomic
def perform_draw(pasanaku):

    # Participantes disponibles para girar (sin ganador y no removidos temporalmente)
    available_participants = Participation.objects.select_for_update().filter(
        pasanaku=pasanaku,
        is_winner=False,
        is_temporarily_removed=False
    )

    if not available_participants.exists():
        return None

    selected_participation = random.choice(list(available_participants))

    draws_before_winner = max(1, pasanaku.draws_before_winner)
    current_step = pasanaku.current_pre_draw_count + 1

    # Si aún no llega al sorteo ganador, remover temporalmente al seleccionado.
    if current_step < draws_before_winner:
        selected_participation.is_temporarily_removed = True
        selected_participation.save(update_fields=['is_temporarily_removed'])

        pasanaku.current_pre_draw_count = current_step
        pasanaku.save(update_fields=['current_pre_draw_count'])

        return {
            'result_type': 'temporary_removed',
            'participation': selected_participation,
            'current_step': current_step,
            'draws_before_winner': draws_before_winner,
        }

    # Ya llegó al sorteo ganador.
    current_draw_count = Draw.objects.filter(pasanaku=pasanaku).count()
    next_draw_number = current_draw_count + 1

    selected_participation.is_winner = True
    selected_participation.winning_position = next_draw_number
    selected_participation.save(update_fields=['is_winner', 'winning_position'])

    Draw.objects.create(
        pasanaku=pasanaku,
        participation=selected_participation,
        draw_number=next_draw_number
    )

    pasanaku.current_pre_draw_count = 0
    pasanaku.save(update_fields=['current_pre_draw_count'])

    return {
        'result_type': 'winner',
        'participation': selected_participation,
        'current_step': current_step,
        'draws_before_winner': draws_before_winner,
    }