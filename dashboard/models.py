from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from opportunity.models import Opportunity
from startups.models import Startup
from talents.models import Talent

CATEGORIES = (
    ('junior_roles', 'Junior'),
    ('mid_level_roles', 'Mid Level'),
    ('senior_roles', 'Senior')
)

STATUS = (
    ('shortlisted', 'shortlisted'),
    ('rejected', 'rejected'),
    ('reviewing', 'reviewing'),
    ('interviewed', 'interviewed'),
    ('offergiven', 'offergiven')
)


class Matches(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matched_on = models.DateTimeField(default=datetime.now)
    status = models.CharField(choices=STATUS, max_length=100, default='reviewing')
    opportunity = models.ManyToManyField(Opportunity)
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, null=True, blank=True)
    startup = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_opportunity(self):
        return self.opportunity.first()

    class Meta:
        verbose_name_plural = 'Matches'

    @property
    def get_rating(self):
        rating = Rating.objects.filter(rating_for=self.talent)

        sum_of_user_rates = sum(rating.values_list('rating_value', flat=True))  # --> rating for one user filtered above

        all_ratings_to_talent = rating.count() * 5  # --> getting number of all ratings for a filtered user
        try:
            rates = round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
        except ZeroDivisionError:
            rates = 0
        return rates


class Thread(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{str(self.sender)} and {str(self.receiver)}"


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, verbose_name='sender', null=True, on_delete=models.CASCADE)
    the_message = models.TextField()
    sent_on = models.DateTimeField(default=datetime.now)

    # def __str__(self):
    #     return f"{str( self.thread.sender)},{str( self.thread.receiver)}"


class Rating(models.Model):
    rating_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_for = models.ForeignKey(Talent, on_delete=models.CASCADE)
    rating_date = models.DateTimeField(default=datetime.now)
    rating_value = models.FloatField(max_length=100)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.rating_for)

    class Meta:
        ordering = ("-id",)


class Package(models.Model):
    CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )

    name = models.CharField(max_length=100)
    charge = models.CharField(max_length=100, default=0)
    opportunity_listing = models.CharField(max_length=100, choices=CHOICES, default='No')
    talent_due_deligency = models.CharField(max_length=100, choices=CHOICES, default='No')
    legal = models.CharField(max_length=100, choices=CHOICES, default='No')
    payroll = models.CharField(max_length=100, choices=CHOICES, default='No')
    category = models.CharField(choices=CATEGORIES, max_length=100, null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.category}"

    @property
    def get_category(self):
        return self.get_category_display()


class PackagePayment(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    package_name = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    opportunities = models.ManyToManyField(Opportunity)
    opportunities_to_post = models.IntegerField(null=True, blank=True)
    amount_paid = models.FloatField(null=True, blank=True)
    txt_ref = models.CharField(max_length=255, null=True, blank=True)
    completed = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    date_paid = models.DateTimeField(null=True, blank=True)
    active_payment = models.BooleanField(default=False)
    can_post = models.BooleanField(default=True)
    auto_created = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.opportunities_to_post == self.active_opportunities.count():
    #         self.closed = True
    #     else:
    #         self.closed = False
    #     self.save()

    def __str__(self):
        return self.user.username

    @property
    def matched_count(self):
        return self.opportunities.filter(expired=False).aggregate(total=Sum("matched"))["total"] or 0

    @property
    def posted_opportunity(self):
        return self.opportunities.count()

    @property
    def active_opportunities(self):
        return self.opportunities.filter(active=True)

    @property
    def inactive_opportunities(self):
        return self.opportunities.count() - self.active_opportunities.count()
