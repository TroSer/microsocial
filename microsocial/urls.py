from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.i18n import set_language


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='microsocial/main.html'), name='main'),
    url(r'^registration/$', TemplateView.as_view(template_name='microsocial/registration.html'), name='registration'),
    url(r'^login/$', TemplateView.as_view(template_name='microsocial/login.html'), name='login'),
    url(r'^password-recovery/$', TemplateView.as_view(template_name='microsocial/password-recovery.html'), name='password-recovery'),
    url(r'', include('person.urls')),
    url(r'^(about/)$', flatpage, name='about'),
    url(r'^(help/)$', flatpage, name='help'),
    url(r'^(vacancies/)$', flatpage, name='vacancies'),
    url(r'^(for-developers/)$', flatpage, name='for-developers'),
    url(r'^(advertising/)$', flatpage, name='advertising'),
    url(r'^i18n/setlang/$', csrf_exempt(set_language), name='set_language'),
    url(r'^admin/', include(admin.site.urls)),
]
