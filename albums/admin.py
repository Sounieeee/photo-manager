"""Django admin configuration for albums app"""
from django.contrib import admin  # type: ignore
from .models import Album, Photo, AlbumCollaborator


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """Admin interface for Album model"""
    
    list_display = ['title', 'owner', 'is_public', 'created_at', 'photo_count']
    list_filter = ['is_public', 'created_at', 'owner']
    search_fields = ['title', 'description', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner')
        }),
        ('Permissions', {
            'fields': ('is_public',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Photos'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Admin interface for Photo model"""
    
    list_display = ['title', 'album', 'uploaded_by', 'uploaded_at']
    list_filter = ['album', 'uploaded_by', 'uploaded_at']
    search_fields = ['title', 'description', 'album__title', 'uploaded_by__username']
    readonly_fields = ['uploaded_at', 'updated_at']
    fieldsets = (
        ('Photo Information', {
            'fields': ('title', 'description', 'image', 'album')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AlbumCollaborator)
class AlbumCollaboratorAdmin(admin.ModelAdmin):
    """Admin interface for AlbumCollaborator model"""
    
    list_display = ['user', 'album', 'role', 'added_at']
    list_filter = ['role', 'added_at', 'album']
    search_fields = ['user__username', 'album__title']
    readonly_fields = ['added_at']
    fieldsets = (
        ('Collaboration Settings', {
            'fields': ('album', 'user', 'role')
        }),
        ('Metadata', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        }),
    )
