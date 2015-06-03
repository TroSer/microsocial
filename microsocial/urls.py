from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.i18n import set_language
from microsocial import views


urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'', include('person.urls')),
    url(r'', include('auths.urls')),
    url(r'^(about/)$', flatpage, name='about'),
    url(r'^(help/)$', flatpage, name='help'),
    url(r'^(vacancies/)$', flatpage, name='vacancies'),
    url(r'^(for-developers/)$', flatpage, name='for-developers'),
    url(r'^(terms-of-use/)$', flatpage, name='terms-of-use'),
    url(r'^(advertising/)$', flatpage, name='advertising'),
    url(r'^i18n/setlang/$', csrf_exempt(set_language), name='set_language'),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
