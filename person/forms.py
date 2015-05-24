from django import forms
from microsocial.forms import BootstrapFormMixin
from person.models import User


class PersonForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)