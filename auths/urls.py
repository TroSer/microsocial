from django.conf.urls import url
from auths import views

urlpatterns = [
    #url(r'^login/$', views.login_view, name='login'),
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'auths/login.html'}
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
        kwargs={'next_page': 'login'}
    ),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^registration/(?P<token>.+)$', views.RegistrationConfirmView.as_view(), name='registration_confirm'),
    url(r'^password-recovery/$', views.PasswordRecoveryView.as_view(), name='password_recovery'),
]