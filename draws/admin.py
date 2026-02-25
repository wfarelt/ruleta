from django.contrib import admin
from .models import Draw


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ('pasanaku', 'participation', 'draw_number', 'draw_date')
    list_filter = ('pasanaku',)
    search_fields = ('participation__participant__full_name',)