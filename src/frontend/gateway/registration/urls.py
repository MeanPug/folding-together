from django.urls import path
from registration import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('about/', views.AboutView.as_view(), name='about'),
]
