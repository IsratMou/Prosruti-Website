from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


class Counselor(models.Model):
    """Model for counselor profiles"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="counselor_profile")
    bio = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=200)
    experience = models.PositiveIntegerField(default=0, help_text="Experience in years")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - Counselor"

    def get_absolute_url(self):
        return reverse('counseling:counselor_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-experience']


class Session(models.Model):
    """Model for counseling sessions"""
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    SESSION_TYPE_CHOICES = (
        ('video', 'Video Call'),
        ('voice', 'Voice Call'),
        ('text', 'Text Chat'),
        ('in_person', 'In Person'),
    )


counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name="sessions")
client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="counseling_sessions")
title = models.CharField(max_length=200)
description = models.TextField(blank=True, null=True)
session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='text')
status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
scheduled_at = models.DateTimeField()
duration = models.PositiveIntegerField(default=60, help_text="Duration in minutes")
meeting_link = models.URLField(blank=True, null=True, help_text="Link for online sessions")
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)


def __str__(self):
    return f"Session: {self.title} ({self.get_status_display()})"


def get_absolute_url(self):
    return reverse('counseling:session_detail', kwargs={'pk': self.pk})


@property
def is_past_due(self):
    return timezone.now() > self.scheduled_at


class Meta:
    ordering = ['-scheduled_at']


class SessionNote(models.Model):
    """Model for counselor's notes on sessions"""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    is_private = models.BooleanField(default=True, help_text="Private notes are only visible to the counselor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        visibility = "Private" if self.is_private else "Shared"
        return f"{visibility} Note for {self.session.title}"

    class Meta:
        ordering = ['-created_at']

class Resource(models.Model):
    """Model for counseling resources that can be shared with clients"""
    RESOURCE_TYPE_CHOICES = (
        ('article', 'Article'),
        ('video', 'Video'),
        ('exercise', 'Exercise'),
        ('worksheet', 'Worksheet'),
        ('other', 'Other'),
    )