from django import forms

class NewPostForm(forms.Form):
    content = forms.CharField(label="New Post", widget=forms.Textarea(attrs={'id': 'new-post-input', 'class': 'form-control', 'placeholder': "Create new post", "rows": "3"}))
