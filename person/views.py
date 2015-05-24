# coding=utf-8
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from person.forms import PersonForm
from person.models import User


class PersonProfileView(TemplateView):
    template_name = 'person/profile.html'


class PersonEditView(TemplateView):
    template_name = 'person/profile_edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.instance = get_object_or_404(User, pk=request.user.id)

        self.form = PersonForm(request.POST or None, instance=self.instance)
        return super(PersonEditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonEditView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            saved_instance = self.form.save()
            if not self.instance:
                messages.success(request, ugettext(u'Профиль успешно создан.'))
            else:
                messages.success(request, ugettext(u'Профиль успешно сохранен.'))
            return redirect('profile', person_id=saved_instance.pk)
        return self.get(request, *args, **kwargs)