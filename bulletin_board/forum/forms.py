from django import forms

from .models import Announcement, Response


# Форма для создания объявлений
class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ['title', 'description', 'category', 'content_media']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-input'}),
        }


# Форма для создания откликов
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-input', 'rows': 5})
        }


# Форма для отпраки новостей
class NewsForm(forms.Form):
    subject = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'from-input', 'rows': 4}))

