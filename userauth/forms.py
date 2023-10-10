from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

USER_STATUS = (
    ('talent', 'talent'),
    ('startup', 'startup')
)


class NewUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'User Name'}), required=True,
                               label='Username')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), required=True, label='Email')
    user_type = forms.ChoiceField(choices=USER_STATUS, widget=forms.RadioSelect())
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True,
                                label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), required=True,
                                label='Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=USER_STATUS, widget=forms.RadioSelect())

    class Meta:
        model = Profile
        fields = ('user_type',)
