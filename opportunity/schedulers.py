from django.utils import timezone

from opportunity.models import Opportunity


def check_expired_opportunity():
    print("Checking for opportunities deadlines")
    opportunities = Opportunity.objects.filter(expired=False)
    for opportunity in opportunities:
        if opportunity.deadline < timezone.now():
            opportunity.expired = True
            opportunity.save()
