from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Pasanaku


@require_POST
def configure_pasanaku(request, pasanaku_id):
	pasanaku = get_object_or_404(Pasanaku, id=pasanaku_id)

	pasanaku.name = request.POST.get('name', pasanaku.name).strip()
	pasanaku.start_date = request.POST.get('start_date', pasanaku.start_date)
	pasanaku.total_participants = int(request.POST.get('total_participants', pasanaku.total_participants))
	pasanaku.monthly_amount = request.POST.get('monthly_amount', pasanaku.monthly_amount)
	pasanaku.draws_per_month = int(request.POST.get('draws_per_month', pasanaku.draws_per_month))
	pasanaku.draws_before_winner = int(request.POST.get('draws_before_winner', pasanaku.draws_before_winner))
	pasanaku.status = request.POST.get('status', pasanaku.status)

	if pasanaku.draws_before_winner < 1:
		pasanaku.draws_before_winner = 1

	max_pre_draw_count = max(pasanaku.draws_before_winner - 1, 0)
	pasanaku.current_pre_draw_count = min(pasanaku.current_pre_draw_count, max_pre_draw_count)

	try:
		pasanaku.full_clean()
		pasanaku.save()
	except (ValidationError, ValueError):
		# Keep dashboard flow simple: on invalid data, return without persisting.
		return redirect('dashboard')

	return redirect('dashboard')
