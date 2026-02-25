import random
from django.db import transaction
from pasanaku.models import Participation
from .models import Draw


@transaction.atomic
def perform_draw(pasanaku):

    # Participantes disponibles (que no hayan ganado)
    available_participants = Participation.objects.select_for_update().filter(
        pasanaku=pasanaku,
        is_winner=False
    )

    if not available_participants.exists():
        return None

    # Elegir ganador aleatorio
    winner = random.choice(list(available_participants))

    # Calcular número de sorteo
    current_draw_count = Draw.objects.filter(pasanaku=pasanaku).count()
    next_draw_number = current_draw_count + 1

    # Marcar como ganador
    winner.is_winner = True
    winner.winning_position = next_draw_number
    winner.save()

    # Crear registro del sorteo
    Draw.objects.create(
        pasanaku=pasanaku,
        participation=winner,
        draw_number=next_draw_number
    )

    return winner