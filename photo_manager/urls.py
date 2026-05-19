"""
URL configuration for photo_manager project.
"""
from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore
from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore
from django.views.generic import TemplateView  # type: ignore
from django.contrib.auth.views import LoginView, LogoutView  # type: ignore
from django.contrib.auth.forms import UserCreationForm  # type: ignore
from django.contrib.auth import login  # type: ignore
from django.shortcuts import redirect  # type: ignore
from django.views import View  # type: ignore
from django.contrib import messages  # type: ignore


class RegisterView(View):
    """User registration view"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('albums:album-list')
        form = UserCreationForm()
        from django.shortcuts import render  # type: ignore
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('albums:album-list')
        from django.shortcuts import render  # type: ignore
        return render(request, 'register.html', {'form': form})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('albums/', include('albums.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

