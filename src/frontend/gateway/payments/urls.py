from django.urls import path
from payments import views

urlpatterns = [
    path('donate/', views.DonateView.as_view(), name='donate')
]
