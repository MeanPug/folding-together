from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie
from payments import views

urlpatterns = [
    path('donate/', ensure_csrf_cookie(views.DonateView.as_view()), name='donate'),
    path('recent-donations/', views.RecentDonationsView.as_view(), name='recent_donations'),
    path('donations/<donation_slug>/', views.DonationDetailsView.as_view(), name='donation_details'),
    path('thank-you/', views.DonationReceivedView.as_view(), name='donation_received')
]
