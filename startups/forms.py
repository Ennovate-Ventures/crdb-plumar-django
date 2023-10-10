from django import forms


class ratingForm(forms.Form):
    ratings =  forms.CharField()
    rating_for = forms.CharField()
    comments = forms.CharField()

 
        