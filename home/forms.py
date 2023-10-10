from django import forms


class watchlistForm(forms.Form):
    full_name = forms.CharField()
    email = forms.CharField()
    profession = forms.CharField()
    location = forms.CharField()
    career_background = forms.CharField()


class MyForm(forms.Form):
    pass
