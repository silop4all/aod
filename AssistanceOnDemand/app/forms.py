"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Editor
from django.db.models import *
from tinymce.widgets import TinyMCE


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))




class RegistrationForm(forms.Form):
    """

    """

    name = forms.CharField  (max_length=200,
            widget=forms.TextInput({'class':"form-control",'name': "rg_name", 'id': "rg_name",\
            'autocomplete': 'off',  'placeholder':"the name of user", 'required':True, 'autofocus': True}))

    

class EditorForm(forms.BaseModelForm):
    my_field = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    
    class Meta:
        model = Editor
