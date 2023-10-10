from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

USER_STATUS = (
    ('not_set', 'Not Set'),
    ('talent', 'Talent'),
    ('startup', 'Startup')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='profile_images', default='avatar.png')
    user_type = models.CharField(choices=USER_STATUS, max_length=100, default='not_set')
    location = models.CharField(max_length=100, null=True, blank=True)
    completed = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
