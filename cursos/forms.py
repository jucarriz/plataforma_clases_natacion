from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comentario']
        labels = {
            'comentario': 'Tu opinión sobre el curso'
        }
        widgets = {
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escribí tu feedback aquí...'
            })
        }
