from django import forms
from opportunity.models import Opportunity
from django.contrib.auth.forms import UserChangeForm
from startups.models import Startup
from talents.models import *
from userauth.models import Profile
from django.contrib.auth.models import User

SECTORS = (
    ('select sector', 'select sector'),
    ('Architecture & Construction', 'Architecture & Construction'),
    ('Accountancy and Financial Management', 'Accountancy and Financial Management'),
    ('Business, Consulting and Management', 'Business, Consulting and Management '),
    ('Law and Legal Services', 'Law and Legal Services'),
    ('Non Government Organization', 'Non Government Organization '),
    ('Media and Communications', 'Media and Communications'),
    ('Creative Arts and Design', 'Creative Arts and Design'),
    ('Energy and Utilities', 'Energy and Utilities'),
    ('Engineering and Manufacturing', 'Engineering and Manufacturing'),
    ('Agribusiness', 'Agribusiness'),
    ('Medical and Healthcare', 'Medical and Healthcare'),
    ('Information Technology', 'Information Technology'),
    ('Hospitality and Tourism', 'Hospitality and Tourism'),
    ('Marketing, Advertising and PR', 'Marketing, Advertising and PR'),
    ('Sales', 'Sales'),
    ('Real Estate', 'Real Estate'),
    ('Finance, Retail and Banking Services', 'Finance, Retail and Banking Services'),
    ('Office Management and Human Resources Services', 'Office Management and Human Resources Services'),
    ('Transportation, Distribution & Logistics', 'Transportation, Distribution & Logistics')
)

JOB_CATEGORIES = (
    ('select category', 'select category'),
    ('full time', 'full time'),
    ('remote', 'remote'),
    ('contractual', 'contractual'),
    ('internship', 'internship'),
    ('voluntering', 'voluntering')
)

SALARY = (
    ('select salary range', 'select salary range'),
    ('0 - 500k', '0 - 500k'),
    ('500k - 1M', '500k - 1M'),
    ('1M - 3M', '1M - 3M'),
    ('3M - 5M', '3M - 5M'),
    ('5M - 8M', '5M - 8M'),
    ('8M and More', '8M and More')

)


class oppForm(forms.Form):
    title = forms.CharField()
    category = forms.CharField()
    salary_range = forms.CharField()
    logo = forms.FileField()
    location = forms.CharField()
    deadline = forms.DateTimeField()
    sector = forms.ChoiceField(choices=SECTORS, widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField()
    duties_and_responsibilities = forms.CharField()
    skills_required = forms.CharField()
    experience = forms.CharField()


class editOppForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # company_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    category = forms.ChoiceField(choices=JOB_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}))
    salary_range = forms.ChoiceField(choices=SALARY, widget=forms.Select(attrs={'class': 'form-control'}))
    logo = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    experience = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    deadline = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    sector = forms.ChoiceField(choices=SECTORS, widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'id': 'default'}))
    skills_required = forms.CharField(widget=forms.Textarea(attrs={'id': 'dark'}))
    duties_and_responsibilities = forms.CharField(widget=forms.Textarea(attrs={'id': 'dark2'}))

    class Meta:
        model = Opportunity
        fields = '__all__'
        exclude = ('user', 'date_published')


class userForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-round', 'placeholder': 'username'}),
        label='Username')
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-round', 'placeholder': 'email'}),
        label='email')
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-round', 'placeholder': 'First Name'}),
        label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round',
                                                              'placeholder': 'Last Name'}), label='Last Name')
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserForm2(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-round', 'placeholder': 'username'}),
        label='Username')
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-round', 'placeholder': 'email'}),
        label='email')
    password = None

    class Meta:
        model = User
        fields = ('username', 'email')
        exclude = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control form-control-round'}),
                             label='Profile Photo', required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user', 'user_type', 'location', 'completed', 'verified')


class TalentForm(forms.ModelForm):
    profession = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                                 label='Profession')
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-round', 'rows': 1}),
                            label='About')
    dob = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                          label='Date Of Birth')
    languages = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                                label='Language(s)')
    salary_expectation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                                         label='Salary Expectation')
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}), label='Phone')
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                               label='Location')
    linkedIn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                               label='Linked In')

    class Meta:
        model = Talent
        fields = '__all__'
        exclude = ('user', 'slug', 'views', 'qualified', 'show_badge', 'started_talent_quiz')
        widgets = {
            'category': forms.Select(attrs={'class': 'bootstrap-select form-control'}),
            'profession': forms.Select(attrs={'class': 'bootstrap-select form-control'}),
            'gender': forms.Select(attrs={'class': 'bootstrap-select form-control'}),
            'prefered_work_type': forms.Select(attrs={'class': 'bootstrap-select form-control'}),
            'years_of_experience': forms.Select(attrs={'class': 'bootstrap-select form-control'}),
            'profession_level': forms.Select(attrs={'class': 'bootstrap-select form-control'}),
        }


class StartupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}), label='Name')
    what_we_offer = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-round', 'rows': 10, 'cols': 10}),
        label='What We Offer', required=False)
    logo = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control form-control-round'}), label='Logo',
                           required=False)
    size = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}), label='Size')
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                               label='Category')
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                               label='Location')
    website = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                              label='Website')
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                                   label='Phone Number')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'cols': 10}),
                                  label='Description', required=False)

    class Meta:
        model = Startup
        fields = '__all__'
        exclude = ('user', 'followers', 'registered_on',)


class expForm(forms.ModelForm):
    WORKING = (
        ('No', 'No'),
        ('Yes', "Yes")
    )

    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                                   label='Company Name')
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control form-control-round', 'type': 'date'}), label='Start Date')
    finish_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control form-control-round', 'type': 'date'}), label='End Date')
    still_working = forms.CharField(widget=forms.RadioSelect(choices=WORKING, attrs={}), label='Still Working')
    position = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                               label='Position')
    details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-round', 'rows': 5}),
                              label='Details')

    class Meta:
        model = Experience
        fields = "__all__"
        exclude = ('talent',)


class addexpForm(forms.Form):
    WORKING = (
        ('No', 'No'),
        ('Yes', "Yes")
    )

    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                                   label='Company Name')
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control form-control-round', 'type': 'date'}), label='Start Date')
    finish_date = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'class': 'form-control form-control-round', 'type': 'date'}), label='End Date')
    still_working = forms.CharField(widget=forms.RadioSelect(choices=WORKING, attrs={}), label='Still Working')
    position = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-round'}),
                               label='Position')
    details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-round', 'rows': 5}),
                              label='Details')

    # class Meta:
    #     model = Experience
    #     fields = "__all__"
    #     exclude = ('talent',)


class AddEduForm(forms.Form):
    speciality = forms.CharField()
    start_date = forms.CharField()
    end_date = forms.CharField()
    school_name = forms.CharField()
    details = forms.CharField()


class AddSkillForm(forms.Form):
    skill = forms.CharField()
    experience = forms.CharField()


class PaymentForm(forms.Form):
    posted_opportunity = forms.CharField()
    pack_name = forms.CharField()
    pack_id = forms.IntegerField()
    name = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    listing_name = forms.CharField()
