# coding=utf-8
from django.contrib import messages
from django.contrib.auth.views import login, logout
from django.core.signing import Signer, BadSignature
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views.generic.base import TemplateView, RedirectView
from auths.forms import RegistrationForm
from microsocial import settings
from person.models import User
from django.utils.translation import ugettext_lazy as _

# def login_view(request):
#     if request.user.is_authenticated():
#         return redirect('main')
#     response = login(request, 'auths/login.html')
#     if request.user.is_authenticated():
#         if 'remember_me' not in request.POST:
#             request.session.set_expiry(0)
#     return response
#
# def logout_view(request):
#     return logout(request, next_page='login')

#
# def login_view(request):
#     context = RequestContext(request)
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(email=email, password=password)
#         if user:
#             if user.is_activate:
#                 login(request, user)
#                 return HttpResponseRedirect('main')
#             else:
#                 return HttpResponse("Your account is disabled")
#         else:
#             return HttpResponse("Invalid login details")
#     else:
#         return render_to_response('auths/login.html', {}, context)
        #return render(request, 'auths/login.html')


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
