from django.db import models
from pasanaku.models import Pasanaku, Participation


class Draw(models.Model):

    pasanaku = models.ForeignKey(
        Pasanaku,
        on_delete=models.CASCADE,
        related_name='draws'
    )

    participation = models.ForeignKey(
        Participation,
        on_delete=models.CASCADE,
        related_name='draws'
    )

    draw_number = models.IntegerField()

    draw_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['draw_number']
        verbose_name = "Draw"
        verbose_name_plural = "Draws"
        unique_together = ('pasanaku', 'draw_number')

    def __str__(self):
        return f"{self.pasanaku.name} - Draw #{self.draw_number}"