from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

from sandbox.settings import MATCHES_MODEL, OPPORTUNITY_MODEL
from talents.models import Talent

Matches = MATCHES_MODEL
Opportunity = OPPORTUNITY_MODEL


class Startup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    size = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    logo = models.FileField(upload_to='startup_images', null=True)
    registered_on = models.DateTimeField(default=datetime.now)
    category = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=100, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='followers')
    description = models.TextField(null=True)
    what_we_offer = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

    @property
    def get_rating(self):
        rating = self.startup_rating_set.all()

        sum_of_user_rates = sum(rating.values_list('rating_value', flat=True))  # --> rating for one user filtered above

        all_ratings_to_talent = rating.count() * 5  # --> getting number of all ratings for a filtered user
        try:
            rates = round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
        except ZeroDivisionError:
            rates = 0
        return rates

    @property
    def get_required_skills(self):
        return self.skills_required_set.all()

    @property
    def get_opportunities(self):
        return self.opportunity_set.all()


class Skills_Required(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill

    class Meta:
        verbose_name_plural = "Skills_Required"


class Startup_Rating(models.Model):
    rating_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_for = models.ForeignKey(Startup, on_delete=models.CASCADE)
    rating_date = models.DateTimeField(default=datetime.now)
    rating_value = models.FloatField(max_length=100)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.rating_for)


class ZoomMeeting(models.Model):
    meeting_id = models.IntegerField(null=True)
    meeting_uuid = models.CharField(max_length=100, null=True)
    host_id = models.CharField(max_length=128, null=True)
    host_email = models.EmailField()
    status = models.CharField(max_length=128, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_url = models.URLField(null=True, max_length=1028)
    join_url = models.URLField(null=True)
    agenda = models.CharField(max_length=1028)
    default_password = models.BooleanField(default=True)
    duration = models.IntegerField(default=60)
    encrypted_password = models.CharField(max_length=128, null=True)
    password = models.CharField(max_length=100, null=True)
    pre_schedule = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True)
    schedule_for = models.EmailField(null=True, blank=True)
    allow_multiple_devices = models.BooleanField(default=True)
    auto_recording = models.CharField(max_length=128, default='cloud')
    contact_name = models.CharField(max_length=1028, null=True)
    contact_email = models.EmailField(null=True)
    email_notification = models.BooleanField(default=True)
    join_before_host = models.BooleanField(default=False)
    timezone = models.CharField(default='Africa/Nairobi', max_length=128)
    topic = models.CharField(max_length=1028, null=True)
    interviewer = models.ForeignKey(Startup, on_delete=models.SET_NULL, null=True)
    interviewer_attended = models.BooleanField(default=False)
    interviewee = models.ForeignKey(Talent, on_delete=models.SET_NULL, null=True)
    interviewee_attended = models.BooleanField(default=False)
    match = models.ForeignKey(Matches, on_delete=models.CASCADE, null=True)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, null=True, blank=True)
    first_reminder_sent = models.BooleanField(default=False)
    second_reminder_sent = models.BooleanField(default=False)

    # can_join = models.BooleanField(default=False)

    def __str__(self):
        return self.agenda

    class Meta:
        ordering = ("-id",)
        indexes = [
            models.Index(
                fields=["interviewer", "interviewee"]
            )
        ]
