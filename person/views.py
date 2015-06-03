# coding=utf-8
from django.contrib import messages
from django.contrib.auth import BACKEND_SESSION_KEY, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from person.forms import PersonForm, UserPasswordChangeForm, UserEmailChangeForm
from person.models import User


class PersonProfileView(TemplateView):
    template_name = 'person/profile.html'


class PersonEditView(TemplateView):
    template_name = 'person/profile_edit.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        action = request.POST.get('action')
        self.profile_form = PersonForm(
            (request.POST if action == 'profile' else None),
            (request.FILES if action == 'profile' else None),
            prefix='profile', instance=request.user
        )
        self.password_form = UserPasswordChangeForm(request.user, (request.POST if action == 'password' else None),
                                                    prefix='password')
        self.email_form = UserEmailChangeForm(request.user, (request.POST if action == 'email' else None),
                                                    prefix='email')
        return super(PersonEditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonEditView, self).get_context_data(**kwargs)
        context['profile_form'] = self.profile_form
        context['password_form'] = self.password_form
        context['email_form'] = self.email_form
        return context

    def post(self, request, *args, **kwargs):
        if self.profile_form.is_valid():
            self.profile_form.save()
            messages.success(request, ugettext(u'Профиль успешно сохранен.'))
            return redirect(request.path)
        elif self.password_form.is_valid():
            self.password_form.save()
            request.user.backend = request.session[BACKEND_SESSION_KEY]
            login(request, request.user)
            messages.success(request, ugettext(u'Пароль успешно сохранен.'))
            return redirect(request.path)
        elif self.email_form.is_valid():
            self.email_form.save()
            messages.success(request, ugettext(u'Email успешно сохранен.'))
            return redirect(request.path)
        return self.get(request, *args, **kwargs)