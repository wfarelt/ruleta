from django.shortcuts import render
from pasanaku.models import Pasanaku, Participation
from draws.models import Draw
from participants.models import Participant
from django.db.models import Count


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

	pasanakus_participants = Pasanaku.objects.annotate(
		participants_count=Count('participations')
	).order_by('-participants_count')[:10]

	return render(request, 'core/dashboard.html', {
		'total_pasanakus': total_pasanakus,
		'total_participants': total_participants,
		'total_draws': total_draws,
		'recent_draws': recent_draws,
		'recent_winners': recent_winners,
		'pasanakus_participants': pasanakus_participants,
	})
