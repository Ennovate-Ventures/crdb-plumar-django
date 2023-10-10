from django import forms
from dashboard.models import Rating

class ratingForm(forms.Form):
    ratings =  forms.CharField()
    rating_for = forms.CharField()
    comments = forms.CharField()

    class Meta:
        model = Rating
        