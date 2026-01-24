"""
URL configuration for lesson_drf project.

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
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

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
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')), # Ścieżki do logowania/odświeżania JWT
    path('auth/protected/', views.protected_view),
    path('auth/protectedclass/', views.ProtectedView.as_view()),
    path('__debug__/', include('debug_toolbar.urls')),
    path('complex_view/', views.complex_view),
    path('complex_query/', views.task_7_view),
    # (28) Ścieżki do dokumentacji
    # Zwraca plik schematu .yaml
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Widok Swagger UI (rekomendowany)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Alternatywny widok ReDoc
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/generate-report/', views.generate_report_api_view),
    # (29) Zadanie 1
    path('api/hello-celery/', views.hello_celery),
    # (29) Zadanie 2
    path('api/multiply/', views.multiply_view, name='multiply'),
    # (29) Zadanie 3
    path('api/log-timestamp/', views.log_timestamp_view),
    # (29) Zadanie 5
    path('api/count-users/', views.count_users_view),
    # (29) Zadanie 7
    path('api/update-last-login/<int:user_id>/', views.update_user_last_login_view),
    # (29) Zadanie 8
    path('api/process-video/', views.process_video_view),
    # (29) Zadanie 10
    path('api/send-email/<int:notification_id>/', views.send_email_notification_view),
    # (29) Zadanie 11
    path('api/start-task/', views.start_long_task_view), # otrzymam task_id
    path('task-status/<task_id>/', views.task_status_view),
    # (29) Zadanie 14
    path('api/generate-users-csv/', views.generate_users_csv_view),
    path('api/users-csv-status/<task_id>/', views.users_csv_status_view),
    # (29) Zadanie 15
    path('api/retry-failing-request/', views.retry_failing_request_view),
    path('api/retry-status/<task_id>/', views.retry_task_status_view),
    # (29) Zadanie 16
    path('api/upload-image/', views.UploadImageView.as_view()),
    path('api/image-status/<int:image_id>/', views.image_status_view),
    # (29) Zadanie 17
    path('api/run-chain/', views.run_chain_view),
    # (29) Zadanie 20
    path('api/logentry-process/', views.create_logentry_and_process),

]

# (29) Zadanie 14 (dla dev, żeby serwować media)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
