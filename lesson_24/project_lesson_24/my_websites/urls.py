"""
URL configuration for my_websites project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home_view, name='home'),
    path("admin/", admin.site.urls),
    path("blog/", include('blog.urls')),
    path("cars/", include('cars.urls')),
    path('register/', views.register, name='register'),
    # (24) Zadanie 2
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', next_page=None), name='logout'),
    # (24) Zadanie 3
    path('profile/', views.profile, name='profile'),
    # (24) Zadanie 8
    path('profile/password/change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('profile/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('all/', views.admin_user_list, name='all')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

""" (24) Zadanie 7
- Django przekierowuje użytkownika po zalogowaniu na stronę, z której przyszedł, korzystając z parametru next w adresie URL. 
- Gdy niezalogowany użytkownik próbuje wejść na stronę wymagającą autoryzacji 
(np. /profile/), Django dodaje do adresu logowania parametr ?next=/profile/. 
- Po wysłaniu formularza logowania wartość next jest przekazywana w ukrytym polu i LoginView używa jej do przekierowania na właściwą stronę. 
- Jeśli parametr next nie istnieje, Django kieruje użytkownika na domyślną stronę określoną w LOGIN_REDIRECT_URL.
"""