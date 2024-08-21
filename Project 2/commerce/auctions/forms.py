from .models import Category

from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(label="Listing Title", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Title"}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter Listing Description"}))
    starting_price = forms.DecimalField(label="Starting Price", decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Enter Starting Price"}))
    image_url = forms.URLField(label="Image URL", required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': "Enter Image URL (Optional)"}))
    choices = [(category.id, category.name) for category in Category.objects.all()]
    category = forms.ChoiceField(label="Category", choices=choices, widget=forms.Select(attrs={'class': 'form-control', 'styles': 'max-width: 30%;'}))

class NewBidForm(forms.Form):
    amount = forms.DecimalField(label="Bid amount", decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Bid Amount"}))

class NewCommentForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter a comment"}))
