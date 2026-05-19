"""Models for photo albums with RBAC"""
from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.core.exceptions import PermissionDenied  # type: ignore


class Album(models.Model):
    """Album model with role-based access control"""
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]
    
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_albums')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False, help_text='Public albums are visible to all users')
    cover_image = models.ImageField(upload_to='albums/covers/', blank=True, null=True, help_text='Upload a cover photo for this album')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return self.title
    
    def can_edit(self, user):
        """Check if user can edit this album"""
        if not user.is_authenticated:
            return False
        if self.owner == user:
            return True
        return self.collaborators.filter(user=user, role__in=['owner', 'editor']).exists()
    
    def can_view(self, user):
        """Check if user can view this album"""
        if not user.is_authenticated:
            return self.is_public
        if self.owner == user:
            return True
        if self.collaborators.filter(user=user).exists():
            return True
        return self.is_public
    
    def can_delete(self, user):
        """Check if user can delete this album"""
        return self.owner == user and user.is_authenticated
    
    def get_photos_count(self):
        """Get the count of photos in this album"""
        return self.photos.count()


class AlbumCollaborator(models.Model):
    """Manage album access and permissions for users"""
    
    ROLE_CHOICES = Album.ROLE_CHOICES
    
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='collaborators')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_collaborations')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['album', 'user']
        ordering = ['added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.album.title} ({self.role})"


class Photo(models.Model):
    """Photo model with metadata"""
    
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='albums/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['album', '-uploaded_at']),
        ]
    
    def __str__(self):
        return self.title or f"Photo {self.id}"
    
    def can_delete(self, user):
        """Check if user can delete this photo"""
        if not user.is_authenticated:
            return False
        if user == self.uploaded_by:
            return True
        return self.album.can_edit(user)
