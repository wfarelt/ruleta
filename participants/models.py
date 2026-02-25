from django.db import models

# Create your models here.

class Participant(models.Model):
    full_name = models.CharField(
        max_length=150,
        verbose_name="Full Name"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['full_name']
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def __str__(self):
        return self.full_name