from django.forms import ModelForm
from .models import Passw


class NewPasswordForm(ModelForm):
    class Meta:
        model = Passw
        fields = ['title']