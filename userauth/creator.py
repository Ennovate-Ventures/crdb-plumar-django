# import profile
# from urllib import request
# from django.db.models.signals import post_save
# from startups.models import Startup
# from django.contrib.auth.models import User

# def create_startup(sender, **kwargs):
#     if kwargs['created']:
#        starup  = Startup.objects.create(user=kwargs['instance'])

# post_save.connect(create_startup, sender=User)
