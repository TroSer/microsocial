# coding=utf-8
from django.contrib import messages
from django.contrib.auth.views import login, logout
from django.contrib.auth import login as auth_login
from django.core.signing import Signer, BadSignature, TimestampSigner
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views.generic.base import TemplateView, RedirectView
from auths.forms import RegistrationForm, PasswordRecoveryForm, LoginForm, NewPasswordForm
from microsocial import settings
from person.models import User
from django.utils.translation import ugettext_lazy as _


def login_view(request):
    if request.user.is_authenticated():
        return redirect('main')
    return login(request, 'auths/login.html', authentication_form=LoginForm)

#
# def logout_view(request):
#     return logout(request, next_page='login')


class RegistrationView(TemplateView):
    template_name = 'auths/registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('main')
        self.form = RegistrationForm(request.POST or None)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['form'] = self.form
        if 'registered_user_id' in self.request.session:
            context['registered_user'] = User.objects.get(pk=self.request.session.pop('registered_user_id'))
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save()
            user.send_registration_email()
            request.session['registered_user_id'] = user.pk
            return redirect(request.path)
        return self.get(request, *args, **kwargs)


class RegistrationConfirmView(RedirectView):
    url = reverse_lazy(settings.LOGIN_URL)
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            raise Http404
        try:
            user_id = Signer(salt='registration-confirm').unsign(kwargs['token'])
        except BadSignature:
            raise Http404
        user = User.objects.get(pk=user_id)
        if user.confirmed_registration:
            raise Http404
        user.confirmed_registration = True
        user.save(update_fields=('confirmed_registration',))
        messages.success(request, _(u'Регистрация успешно подтверждена.'))
        return super(RegistrationConfirmView, self).dispatch(request, *args, **kwargs)


class PasswordRecoveryView(TemplateView):
    template_name = 'auths/password-recovery.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('main')
        self.form = PasswordRecoveryForm(request.POST or None)
        return super(PasswordRecoveryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PasswordRecoveryView, self).get_context_data(**kwargs)
        context['form'] = self.form
        if 'pwd_recovery_user_id' in self.request.session:
            context['pwd_recovery_user'] = User.objects.get(pk=self.request.session.pop('pwd_recovery_user_id'))
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.get_user()
            user.send_password_recovery_email()
            request.session['pwd_recovery_user_id'] = user.pk
            return redirect(request.path)
        return self.get(request, *args, **kwargs)


class PasswordRecoveryConfirmView(TemplateView):
    template_name = 'auths/password-recovery-form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('main')
        try:
            data = TimestampSigner(salt='password-recovery-confirm').unsign(kwargs['token'], max_age=(48 * 3600))
            user_id, last_login_hash = data.split(':')
        except (BadSignature, ValueError):
            raise Http404
        user = User.objects.get(pk=user_id)
        if user.get_last_login_hash() != last_login_hash:
            raise Http404
        if not user.confirmed_registration:
            user.confirmed_registration = True
            user.save(update_fields=('confirmed_registration', ))
        self.form = NewPasswordForm(user, request.POST or None)
        return super(PasswordRecoveryConfirmView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PasswordRecoveryConfirmView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            self.form.user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, self.form.user)
            return redirect('profile_edit')
        return self.get(request, *args, **kwargs)