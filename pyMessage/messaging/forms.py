from django import forms
from .models import ImageMessage

class ImageForm(forms.Form):
    image = forms.ImageField(label='Image', required=False)
    
    class Meta:
        model = ImageMessage
        fields = ('image',)
        widgets = {
            'sender': forms.HiddenInput(),
            'receiver': forms.HiddenInput(),
            }