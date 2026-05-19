"""URL configuration for albums app"""
from django.urls import path  # type: ignore
from . import views

app_name = 'albums'

urlpatterns = [
    # Album URLs
    path('', views.AlbumListView.as_view(), name='album-list'),
    path('create/', views.AlbumCreateView.as_view(), name='album-create'),
    path('<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album-edit'),
    path('<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),
    
    # Photo URLs
    path('<int:album_pk>/photos/create/', views.PhotoCreateView.as_view(), name='photo-create'),
    path('<int:album_pk>/photos/<int:photo_pk>/edit/', views.PhotoUpdateView.as_view(), name='photo-edit'),
    path('<int:album_pk>/photos/<int:photo_pk>/delete/', views.PhotoDeleteView.as_view(), name='photo-delete'),
    
    # Collaborator URLs
    path('<int:album_pk>/collaborators/', views.AlbumCollaboratorsView.as_view(), name='album-collaborators'),
    path('<int:album_pk>/collaborators/add/', views.AddCollaboratorView.as_view(), name='add-collaborator'),
    path('<int:album_pk>/collaborators/<int:collaborator_pk>/remove/', views.RemoveCollaboratorView.as_view(), name='remove-collaborator'),
]
