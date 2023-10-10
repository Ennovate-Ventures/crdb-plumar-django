import math

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

from startups.models import Startup, Matches

# Create your models here.
JOB_CATEGORIES = (
    ('full time', 'full time'),
    ('remote', 'remote'),
    ('contractual', 'contractual'),
    ('internship', 'internship'),
    ('voluntering', 'voluntering'),
    ('freelance', 'freelance'),
    ('part-time', 'part-time'),
    ('temporary', 'temporary'),
    ('internship', 'internship')
)

SALARY = (
    ('0 - 500k', '0 - 500k'),
    ('500k - 1M', '500k - 1M'),
    ('1M - 3M', '1M - 3M'),
    ('3M - 5M', '3M - 5M'),
    ('5M - 8M', '5M - 8M'),
    ('8M and More', '8M and More')

)

SECTORS = (
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

EXPIRE = (

    ('Yes', 'Yes'),
    ('No', 'No')
)


class Opportunity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # company_name = models.CharField(max_length=100, null=True,  blank=True)
    category = models.CharField(max_length=100, choices=JOB_CATEGORIES)
    salary_range = models.CharField(max_length=100, choices=SALARY)
    experience = models.CharField(max_length=100, default="1")
    logo = models.FileField(upload_to='job_logo', null=True, blank=True)
    location = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    skills_required = HTMLField(null=True, blank=True)
    duties_and_responsibilities = HTMLField(null=True, blank=True)
    sector = models.CharField(max_length=100, choices=SECTORS)
    date_published = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    matched = models.IntegerField(default=0)
    marked = models.ManyToManyField(User, related_name='likes')
    startup_name = models.ForeignKey(Startup, on_delete=models.SET_NULL, null=True)
    expired = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Opportunities'

    @property
    def count(self):
        return self.id.count

    @property
    def status(self):
        result = self.deadline > timezone.now()
        status: str
        if not self.active:
            status = "Not Paid"
        elif result:
            status = 'Active'
            self.expired = False
        else:
            self.expired = True
            status = 'Expired'
        self.save()
        return status

    @property
    def published(self):
        now = timezone.now()

        diff = now - self.date_published
        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + " second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        if 1 <= diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if 30 <= diff.days < 365:
            months = math.floor(diff.days / 30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

    @property
    def get_skills(self):
        skill = Skills.objects.filter(opportunity=self.title)
        return skill


class Skills(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill

    class Meta:
        verbose_name_plural = "Skills"
