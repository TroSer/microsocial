from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^profile/$', TemplateView.as_view(template_name='person/profile.html'), name='profile'),
]
