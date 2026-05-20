"""Views for photo albums with RBAC"""
from django.shortcuts import get_object_or_404, redirect  # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # type: ignore
from django.urls import reverse_lazy  # type: ignore
from django.http import Http404  # type: ignore
from django.contrib import messages  # type: ignore
from django.db.models import Q  # type: ignore
import logging

from .models import Album, Photo, AlbumCollaborator
from .forms import AlbumForm, PhotoForm, AlbumCollaboratorForm

logger = logging.getLogger(__name__)


# Mixin for checking album access
class AlbumAccessMixin(UserPassesTestMixin):
    """Mixin to check if user has access to the album"""
    
    def test_func(self):
        album = self.get_album()
        return album.can_view(self.request.user)
    
    def get_album(self):
        if hasattr(self, 'object') and isinstance(self.object, Album):
            return self.object
        return get_object_or_404(Album, pk=self.kwargs.get('album_pk', self.kwargs.get('pk')))
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this album.")
        return redirect('albums:album-list')


class AlbumEditMixin(UserPassesTestMixin):
    """Mixin to check if user can edit the album"""
    
    def test_func(self):
        album = self.get_album()
        return album.can_edit(self.request.user)
    
    def get_album(self):
        if hasattr(self, 'object') and isinstance(self.object, Album):
            return self.object
        return get_object_or_404(Album, pk=self.kwargs.get('album_pk', self.kwargs.get('pk')))
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this album.")
        return redirect('albums:album-list')


class AlbumOwnerMixin(UserPassesTestMixin):
    """Mixin to check if user is the album owner"""
    
    def test_func(self):
        album = self.get_album()
        return album.can_delete(self.request.user)
    
    def get_album(self):
        if hasattr(self, 'object') and isinstance(self.object, Album):
            return self.object
        return get_object_or_404(Album, pk=self.kwargs.get('album_pk', self.kwargs.get('pk')))
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to perform this action.")
        return redirect('albums:album-list')


# Album Views
class AlbumListView(LoginRequiredMixin, ListView):
    """List all albums accessible to the user"""
    
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'
    paginate_by = 12
    login_url = 'login'
    
    def get_queryset(self):
        """Get albums that user owns or collaborates on, plus public albums"""
        user = self.request.user
        return Album.objects.filter(
            Q(owner=user) | 
            Q(collaborators__user=user) |
            Q(is_public=True)
        ).distinct().prefetch_related('collaborators__user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owned_count'] = Album.objects.filter(owner=self.request.user).count()
        context['collaborated_count'] = AlbumCollaborator.objects.filter(
            user=self.request.user
        ).count()
        return context


class AlbumDetailView(AlbumAccessMixin, DetailView):
    """View album details and photos"""
    
    model = Album
    template_name = 'albums/album_detail.html'
    context_object_name = 'album'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.get_object()
        context['photos'] = album.photos.all()
        context['collaborators'] = album.collaborators.all()
        context['can_edit'] = album.can_edit(self.request.user)
        context['can_delete'] = album.can_delete(self.request.user)
        # Provide an explicit photo count to ensure templates show accurate stats
        try:
            context['photo_count'] = album.photos.count()
        except Exception:
            context['photo_count'] = 0
        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    """Create a new album"""
    
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Album '{form.instance.title}' created successfully!")
        return response
    
    def get_success_url(self):
        return reverse_lazy('albums:album-detail', kwargs={'pk': self.object.pk})


class AlbumUpdateView(AlbumEditMixin, LoginRequiredMixin, UpdateView):
    """Update an album"""
    
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'
    pk_url_kwarg = 'pk'
    login_url = 'login'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Album '{form.instance.title}' updated successfully!")
        return response
    
    def get_success_url(self):
        return reverse_lazy('albums:album-detail', kwargs={'pk': self.object.pk})


class AlbumDeleteView(AlbumOwnerMixin, LoginRequiredMixin, DeleteView):
    """Delete an album"""
    
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('albums:album-list')
    login_url = 'login'
    
    def delete(self, request, *args, **kwargs):
        album_title = self.get_object().title
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Album '{album_title}' deleted successfully!")
        return response


# Photo Views
class PhotoCreateView(AlbumEditMixin, LoginRequiredMixin, CreateView):
    """Upload a photo to an album"""
    
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'
    login_url = 'login'
    
    def get_album(self):
        return get_object_or_404(Album, pk=self.kwargs['album_pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.get_album()
        return context
    
    def form_valid(self, form):
        form.instance.album_id = self.kwargs['album_pk']
        form.instance.uploaded_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Photo uploaded successfully!")
        try:
            # Expose the saved image URL in messages for easier verification in production logs/UI
            img_url = self.object.image.url
            messages.info(self.request, f"Uploaded image URL: {img_url}")
            # Log details for server-side debugging
            logger.info("Photo uploaded: name=%s url=%s album_id=%s uploaded_by=%s", self.object.image.name, img_url, self.object.album_id, self.request.user.username)
            try:
                album_count = self.object.album.photos.count()
                logger.info("Album %s now has %d photos", self.object.album_id, album_count)
            except Exception:
                logger.debug("Could not compute album photo count for album_id=%s", self.object.album_id)
        except Exception:
            # If the storage backend didn't populate a URL, silently continue
            logger.exception("Failed to read uploaded photo URL after save")
        return response
    
    def get_success_url(self):
        return reverse_lazy('albums:album-detail', kwargs={'pk': self.kwargs['album_pk']})


class PhotoUpdateView(AlbumEditMixin, LoginRequiredMixin, UpdateView):
    """Update photo details"""
    
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'
    pk_url_kwarg = 'photo_pk'
    login_url = 'login'
    
    def get_album(self):
        return self.get_object().album
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.get_object().album
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Photo updated successfully!")
        return response
    
    def get_success_url(self):
        photo = self.get_object()
        return reverse_lazy('albums:album-detail', kwargs={'pk': photo.album.pk})


class PhotoDeleteView(AlbumEditMixin, LoginRequiredMixin, DeleteView):
    """Delete a photo"""
    
    model = Photo
    template_name = 'albums/photo_confirm_delete.html'
    pk_url_kwarg = 'photo_pk'
    login_url = 'login'
    
    def get_album(self):
        return self.get_object().album
    
    def get_success_url(self):
        album_pk = self.kwargs['album_pk']
        messages.success(self.request, "Photo deleted successfully!")
        return reverse_lazy('albums:album-detail', kwargs={'pk': album_pk})


# Collaborator Views
class AlbumCollaboratorsView(AlbumOwnerMixin, LoginRequiredMixin, ListView):
    """Manage album collaborators"""
    
    template_name = 'albums/collaborators.html'
    context_object_name = 'collaborators'
    paginate_by = 20
    login_url = 'login'
    
    def get_queryset(self):
        album = self.get_album()
        return album.collaborators.all()
    
    def get_album(self):
        return get_object_or_404(Album, pk=self.kwargs['album_pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.get_album()
        context['form'] = AlbumCollaboratorForm()
        return context


class AddCollaboratorView(AlbumOwnerMixin, LoginRequiredMixin, CreateView):
    """Add a collaborator to an album"""
    
    model = AlbumCollaborator
    form_class = AlbumCollaboratorForm
    template_name = 'albums/add_collaborator.html'
    login_url = 'login'
    
    def get_album(self):
        return get_object_or_404(Album, pk=self.kwargs['album_pk'])
    
    def form_valid(self, form):
        album = self.get_album()
        user = form.cleaned_data['user']
        
        # Check if already a collaborator
        if AlbumCollaborator.objects.filter(album=album, user=user).exists():
            messages.warning(self.request, f"{user.username} is already a collaborator on this album.")
            return redirect('albums:album-collaborators', album_pk=album.pk)
        
        # Check if trying to add the owner
        if user == album.owner:
            messages.warning(self.request, "The album owner is already a collaborator.")
            return redirect('albums:album-collaborators', album_pk=album.pk)
        
        form.instance.album = album
        response = super().form_valid(form)
        messages.success(self.request, f"{user.username} added as a collaborator!")
        return response
    
    def get_success_url(self):
        return reverse_lazy('albums:album-collaborators', kwargs={'album_pk': self.kwargs['album_pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.get_album()
        return context


class RemoveCollaboratorView(AlbumOwnerMixin, LoginRequiredMixin, DeleteView):
    """Remove a collaborator from an album"""
    
    model = AlbumCollaborator
    template_name = 'albums/remove_collaborator.html'
    pk_url_kwarg = 'collaborator_pk'
    login_url = 'login'
    
    def get_album(self):
        return self.get_object().album
    
    def get_success_url(self):
        album_pk = self.kwargs['album_pk']
        messages.success(self.request, "Collaborator removed successfully!")
        return reverse_lazy('albums:album-collaborators', kwargs={'album_pk': album_pk})
    
    def delete(self, request, *args, **kwargs):
        collaborator = self.get_object()
        username = collaborator.user.username
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"{username} removed from album collaborators.")
        return response
