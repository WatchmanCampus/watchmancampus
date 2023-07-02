from django import forms
from .models import Tick, Post, Transaction


class TickRegisterForm(forms.ModelForm):

    class Meta:
        model = Tick
        exclude = [
            "ref",
            "img",
            "created_at",
            "attended",
            "post"
        ]


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = [
            "created_at"     
        ]

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ["payment_method", "payment_provider"]