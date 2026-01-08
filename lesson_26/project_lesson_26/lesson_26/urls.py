"""
URL configuration for lesson_26 project.

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
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from api import views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tasks', views.TaskViewSet) # Zarejestruj nasz ViewSet pod adresem /tasks/
router.register(r'products', views.ProductViewSet)
router.register(r'notes', views.NoteViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('api/hello/', views.hello_view),
    path('api/set-name/', views.set_name_view),
    path('api/calculate/', views.calculate_view),
    # (26) Zadanie 4
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')), # Ścieżki do logowania/odświeżania JWT
    path('auth/protected/', views.protected_view),
    path('auth/protectedclass/', views.ProtectedView.as_view()),
    
]
