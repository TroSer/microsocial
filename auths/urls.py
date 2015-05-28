from django.conf.urls import url
from django.contrib.auth.views import logout
from auths import views
from microsocial import settings

urlpatterns = [
    url(
        r'^login/$',
        views.login_view,
        name='login',
    ),
    url(
        r'^logout/$',
        logout,
        name='logout',
        kwargs={'next_page': settings.LOGIN_URL},
    ),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^registration/(?P<token>.+)$', views.RegistrationConfirmView.as_view(), name='registration_confirm'),
    url(r'^password-recovery/$', views.PasswordRecoveryView.as_view(), name='password_recovery'),
]