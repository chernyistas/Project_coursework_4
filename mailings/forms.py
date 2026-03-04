from django import forms
from .models import Mailing
from django.utils import timezone


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "clients"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "clients": forms.SelectMultiple(attrs={"size": "10"}),
        }


    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")


        if start_time and end_time:
            if self.instance is None or self.instance.pk is None:
                if start_time < timezone.now():
                    self.add_error("start_time", "Дата начала не может быть в прошлом")

            if start_time >= end_time:
               self.add_error("end_time","Дата окончания должна быть позже даты начала")

        return cleaned_data