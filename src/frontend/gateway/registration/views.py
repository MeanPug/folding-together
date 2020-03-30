from django.shortcuts import render
from django.views.generic import TemplateView
from payments.models import Donation


class HomeView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['donation_count'] = Donation.objects.count()
        return context
