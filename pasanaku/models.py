from django.db import models
from participants.models import Participant

# Create your models here.

class Pasanaku(models.Model):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Name"
    )

    start_date = models.DateField(
        verbose_name="Start Date"
    )

    total_participants = models.IntegerField(
        verbose_name="Total Participants"
    )

    monthly_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Monthly Amount"
    )

    draws_per_month = models.IntegerField(
        default=2,
        verbose_name="Draws Per Month"
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    rotation_angle = models.FloatField(
        default=0.0,
        verbose_name="Rotation Angle"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Pasanaku"
        verbose_name_plural = "Pasanakus"

    def __str__(self):
        return self.name
    

class Participation(models.Model):

    pasanaku = models.ForeignKey(
        Pasanaku,
        on_delete=models.CASCADE,
        related_name='participations'
    )

    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='participations'
    )

    is_winner = models.BooleanField(
        default=False
    )

    winning_position = models.IntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pasanaku', 'participant')
        ordering = ['created_at']
        verbose_name = "Participation"
        verbose_name_plural = "Participations"

    def __str__(self):
        return f"{self.participant.full_name} - {self.pasanaku.name}"


