from django.db import models


class Watchlist(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    career_background = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class PopularSearch(models.Model):
    keyword = models.CharField(max_length=255, unique=True)
    search_count = models.IntegerField(default=1)

    def __str__(self):
        return self.keyword

    class Meta:
        ordering = ("-search_count",)
        indexes = [
            models.Index(
                fields=["keyword"]
            )
        ]


class Contact(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    company_name = models.CharField(max_length=128, null=True)
    location = models.CharField(max_length=128)
    profession = models.CharField(max_length=128)
    engage_as = models.CharField(max_length=10, choices=(
        ('talent', 'Talent'), ('startup', 'Startup'), ('partner', 'Partner'), ('investor', 'Investor')))

    def __str__(self):
        return self.name


class Project(models.Model):
    full_name = models.CharField(max_length=128)
    company_name = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField()
    country = models.CharField(max_length=13)
    description = models.CharField(max_length=128)
    expectations = models.CharField(max_length=128)
    achievement = models.CharField(max_length=128)
    design = models.FileField(upload_to="projects")
    mockup = models.FileField(upload_to="projects")
    delivery_time = models.CharField(max_length=128)
    budget = models.CharField(max_length=128)
    more_info = models.TextField(max_length=128)

    def __str__(self):
        return self.company_name
