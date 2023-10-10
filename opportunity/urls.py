from django.urls import path

from . import views

urlpatterns = [
    path('opportunities', views.opportunity, name='opportunity'),
    path('opportunity/<int:id>', views.opportunity_details, name='opp_details'),
    path('add-match', views.add_match, name='add_match'),
    path('delete-match/<int:id>', views.remove_match, name="delete_match"),
    path('mark', views.mark, name='mark')
]
