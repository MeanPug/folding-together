from django.shortcuts import render
from django.views.generic import TemplateView
import json


class DonateView(TemplateView):
    template_name = 'donate.html'

    def post(self, request, *args, **kwargs):
        dat = json.loads(request.body)
