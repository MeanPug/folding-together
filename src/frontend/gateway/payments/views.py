from django.shortcuts import render
from django.views.generic import TemplateView


class DonateView(TemplateView):
    template_name = 'donate.html'
