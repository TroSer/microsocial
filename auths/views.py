from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from auths.forms import RegistrationForm


def login_view(request):
    return render(request, 'auths/login.html')


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
        return context


class PasswordRecoveryView(TemplateView):
    template_name = 'auths/password-recovery.html'
