from django.urls import path
from cars import views

urlpatterns = [
    path('', views.CarListView.as_view(), name='car-list'),
    path('<int:car_id>/', views.car_detail_view, name='car-detail'),
    path('dealers/', views.dealer_list_view, name='dealers'),
    path('dealers/<int:dealer_id>/', views.dealer_detail_view, name='dealer-detail'),
    path('statistics/', views.car_statistics_view, name='car-statistics'),
]

