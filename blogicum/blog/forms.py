from django import forms
from django.core.mail import send_mail
from django.utils import timezone

from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):  # Предзаполнение поля pub_date
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime("%Y-%m-%dT%H:%M")

    class Meta:
        model = Post
        exclude = ("author",)
        widgets = {
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }

    def clean(self):
        super().clean()
        send_mail(
            subject="Новая публикация!",
            message=f"Новая публикация \"{self.cleaned_data.get('title')}\"."
            f"с названием {self.cleaned_data['title']}",
            from_email="publicat_form@blogicum.not",
            recipient_list=["admin@blogicum.not"],
            fail_silently=True,
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
