from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    # path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('', views.landing, name='landing'),
    path('lms', views.lms_home, name='lms'),
    path('terms', views.terms_conditions, name='terms'),
    path('policy', views.privacy_policy, name='policy'),
    path('watchlist', views.watchlist, name="watchlist"),
    path('how-it-works', views.how_it_works, name="how_it_works"),
    path('post-project', views.post_project, name="post_project")

]
