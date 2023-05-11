from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
   class Meta:
       model = Post

       fields = [
           'header',
           'article_text',
           'categories',
           'author_ref'
       ]

   def clean(self):
        cleaned_data = super().clean()
        article_text = cleaned_data.get("article_text")
        if article_text is not None and len(article_text) < 20:
            raise ValidationError({
                "article_text": "Текст статьи не может быть менее 20 символов."
            })

        return cleaned_data