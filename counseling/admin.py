from django.contrib import admin
from .models import Counselor, Session, SessionNote, Resource, SharedResource


@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'qualification', 'experience', 'is_available')
    list_filter = ('is_available', 'specialization')
    search_fields = ('user__username', 'user__email', 'specialization', 'qualification')


class SessionNoteInline(admin.TabularInline):
    model = SessionNote
    extra = 0


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'counselor', 'client', 'session_type', 'status', 'scheduled_at')
    list_filter = ('status', 'session_type', 'scheduled_at')
    search_fields = ('title', 'description', 'counselor__user__username', 'client__username')
    inlines = [SessionNoteInline]
    date_hierarchy = 'scheduled_at'


@admin.register(SessionNote)
class SessionNoteAdmin(admin.ModelAdmin):
    list_display = ('session', 'is_private', 'created_at')
    list_filter = ('is_private', 'created_at')
    search_fields = ('note', 'session__title')


class SharedResourceInline(admin.TabularInline):
    model = SharedResource
    extra = 0


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'created_by', 'is_public', 'created_at')
    list_filter = ('resource_type', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'created_by__user__username')
    inlines = [SharedResourceInline]


@admin.register(SharedResource)
class SharedResourceAdmin(admin.ModelAdmin):
    list_display = ('resource', 'client', 'session', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('resource__title', 'client__username', 'note')


from django.contrib import admin

# Register your models here.
