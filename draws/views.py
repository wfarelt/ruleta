

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
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

    # Recibir el ángulo actual desde el frontend
    rotation_angle = float(request.POST.get('rotation_angle', 0))
    pasanaku.rotation_angle = rotation_angle
    pasanaku.save(update_fields=['rotation_angle'])

    draw_result = perform_draw(pasanaku)

    if not draw_result:
        return JsonResponse({
            "success": False,
            "message": "No participants available."
        })

    selected = draw_result['participation']
    is_winner = draw_result['result_type'] == 'winner'

    return JsonResponse({
        "success": True,
        "result_type": draw_result['result_type'],
        "selected_id": selected.id,
        "selected_name": selected.participant.full_name,
        "position": selected.winning_position,
        "current_step": draw_result['current_step'],
        "draws_before_winner": draw_result['draws_before_winner'],
        "is_winner": is_winner,
        "rotation_angle": pasanaku.rotation_angle
    })



def roulette_view(request, pasanaku_id):
    pasanaku = get_object_or_404(Pasanaku, id=pasanaku_id)

    participants = Participation.objects.filter(
        pasanaku=pasanaku,
        is_winner=False,
        is_temporarily_removed=False
    )

    participants_all = Participation.objects.filter(
        pasanaku=pasanaku
    )

    temporarily_removed_count = Participation.objects.filter(
        pasanaku=pasanaku,
        is_winner=False,
        is_temporarily_removed=True,
    ).count()

    return render(request, 'draws/roulette.html', {
        'pasanaku': pasanaku,
        'participants': participants,
        'participants_all': participants_all,
        'rotation_angle': pasanaku.rotation_angle,
        'temporarily_removed_count': temporarily_removed_count,
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


@require_POST
@csrf_exempt
def reset_draw(request, pasanaku_id):
    pasanaku = get_object_or_404(Pasanaku, id=pasanaku_id)
    # Quitar el flag de ganador y posición a todos los participantes
    Participation.objects.filter(pasanaku=pasanaku).update(
        is_winner=False,
        is_temporarily_removed=False,
        winning_position=None,
    )
    pasanaku.current_pre_draw_count = 0
    pasanaku.save(update_fields=['current_pre_draw_count'])
    # Eliminar los registros de Draw
    Draw.objects.filter(pasanaku=pasanaku).delete()
    return JsonResponse({"success": True})


@require_POST
@csrf_exempt
def restore_temporarily_removed(request, pasanaku_id):
    pasanaku = get_object_or_404(Pasanaku, id=pasanaku_id)

    restored_count = Participation.objects.filter(
        pasanaku=pasanaku,
        is_winner=False,
        is_temporarily_removed=True,
    ).update(is_temporarily_removed=False)

    pasanaku.current_pre_draw_count = 0
    pasanaku.save(update_fields=['current_pre_draw_count'])

    return JsonResponse({"success": True, "restored_count": restored_count})

@require_POST
@csrf_exempt
def save_rotation_angle(request, pasanaku_id):
    pasanaku = get_object_or_404(Pasanaku, id=pasanaku_id)
    rotation_angle = float(request.POST.get('rotation_angle', 0))
    pasanaku.rotation_angle = rotation_angle
    pasanaku.save(update_fields=['rotation_angle'])
    return JsonResponse({"success": True, "rotation_angle": pasanaku.rotation_angle})