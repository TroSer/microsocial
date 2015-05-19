# coding=utf-8
from django.views.generic import TemplateView


class PersonProfileView(TemplateView):
    template_name = 'person/profile.html'