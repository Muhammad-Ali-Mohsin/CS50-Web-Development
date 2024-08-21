from django import forms
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="New Entry Title")
    content = forms.CharField(label="", widget=forms.Textarea())

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title in util.list_entries():
            raise forms.ValidationError("This title is already in use!")
        return title
    
class EditEntryForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea())
