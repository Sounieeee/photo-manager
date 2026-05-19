"""Forms for albums app"""
from django import forms  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from .models import Album, Photo, AlbumCollaborator


class AlbumForm(forms.ModelForm):
    """Form for creating and editing albums"""
    
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Album title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Album description',
                'rows': 4,
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class PhotoForm(forms.ModelForm):
    """Form for uploading photos"""
    
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Photo title (optional)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Photo description (optional)',
                'rows': 3,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }


class AlbumCollaboratorForm(forms.ModelForm):
    """Form for managing album collaborators"""
    
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='Select user to add'
    )
    
    class Meta:
        model = AlbumCollaborator
        fields = ['user', 'role']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
