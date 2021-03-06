from django import forms
from products.models import Comment
from django.forms import ModelForm

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required= False)
    phone_no = forms.RegexField(required= False,regex="^[6-9]\d{9}$")

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email') and not cleaned_data.get('phone_no'):
            raise forms.ValidationError("Enter either email or phone number or both", code= 'invalid')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']