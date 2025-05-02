from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor_display', 'amount', 'currency', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'currency', 'is_anonymous', 'created_at')
    search_fields = ('donor_name', 'donor_email', 'donor_phone', 'transaction_id')
    date_hierarchy = 'created_at'

    def donor_display(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return obj.donor_name or f"User #{obj.user_id}" if obj.user else "Anonymous"

    donor_display.short_description = 'Donor'