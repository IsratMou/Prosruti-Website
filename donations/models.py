from django.db import models
from django.utils import timezone
from django.conf import settings


class Donation(models.Model):
    """Model for storing donation information"""
    PAYMENT_METHODS = (
        ('card', 'Credit/Debit Card'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
        ('bank', 'Bank Transfer'),
    )

    DONATION_STATUSES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donations'
    )  # Anonymous donations allowed

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='BDT')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=DONATION_STATUSES, default='pending')

    donor_name = models.CharField(max_length=100, blank=True)  # For anonymous donors
    donor_email = models.EmailField(blank=True)
    donor_phone = models.CharField(max_length=15, blank=True)

    message = models.TextField(blank=True)  # Optional message from donor
    is_anonymous = models.BooleanField(default=False)  # Option to hide donor name publicly

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_anonymous or not self.donor_name:
            return f"Anonymous donation of {self.amount} {self.currency} ({self.created_at.strftime('%Y-%m-%d')})"
        return f"Donation by {self.donor_name} of {self.amount} {self.currency} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ['-created_at']