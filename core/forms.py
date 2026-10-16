from django import forms

from .models import ContactMessage, WaitlistEntry


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Adınız Soyadınız", "autocomplete": "name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "eposta@sirketiniz.com", "autocomplete": "email"}
            ),
            "subject": forms.TextInput(attrs={"placeholder": "Konu"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Projenizi veya talebinizi anlatın…", "rows": 5}
            ),
        }


class WaitlistForm(forms.ModelForm):
    class Meta:
        model = WaitlistEntry
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "dev@yourcompany.io",
                    "autocomplete": "email",
                    "class": "ni",
                }
            ),
        }
