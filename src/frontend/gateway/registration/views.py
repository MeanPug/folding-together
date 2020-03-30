from django.shortcuts import render
from django.views.generic import TemplateView
from payments.mixins import DonationDataMixin


class HomeView(DonationDataMixin, TemplateView):
    template_name = 'index.html'


class AboutView(DonationDataMixin, TemplateView):
    template_name = 'about.html'
