from django.forms import ModelForm

from chat.models import Visitor, Chat
from django import forms


class LoginForm(ModelForm):
    class Meta:
        model = Visitor
        fields = ["name"]

        labels = {
            "name": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Digite seu nome",
                    "class": "rounded-3xl w-1/2 p-2 lg:p-1 text-center",
                }
            ),
        }


class NewChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = ["name"]

        labels = {
            "name": "Crie um novo chat digitando seu nome aqui",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "rounded-3xl w-2/3 p-1 text-center",
                }
            ),
        }
