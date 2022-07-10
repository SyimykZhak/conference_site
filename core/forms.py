from django import forms
from django.core.exceptions import ValidationError
from .models import Register,Work


class UserForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ('name', 'lastname', 'age', 'email','telephone','addres')


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ('title','work')

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title)>10:
            raise ValidationError("больше 10")
        return title
