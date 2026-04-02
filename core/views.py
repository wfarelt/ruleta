from django.shortcuts import render
from pasanaku.models import Pasanaku, Participation
from draws.models import Draw
from participants.models import Participant
from django.db.models import Count, Q, F, ExpressionWrapper, IntegerField


def dashboard(request):
	total_pasanakus = Pasanaku.objects.count()
	total_participants = Participant.objects.count()
	total_draws = Draw.objects.count()

	recent_draws = Draw.objects.select_related(
		'pasanaku', 'participation__participant'
	).order_by('-draw_date')[:5]

	pasanakus_participants = Pasanaku.objects.annotate(
		participants_count=Count('participations'),
		drawn_games=Count('participations', filter=Q(participations__is_winner=True)),
	).annotate(
		pending_games=ExpressionWrapper(
			F('total_participants') - F('drawn_games'),
			output_field=IntegerField()
		)
	).order_by('-participants_count')[:10]

	return render(request, 'core/dashboard.html', {
		'total_pasanakus': total_pasanakus,
		'total_participants': total_participants,
		'total_draws': total_draws,
		'recent_draws': recent_draws,
		'pasanakus_participants': pasanakus_participants,
	})
