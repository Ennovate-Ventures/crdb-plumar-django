from django.urls import path
from . import views

urlpatterns = [
    path('talents', views.talents, name='talents'),
    path('talent/<str:slug>', views.talent_details, name='talent_details'),
    path('rate/<str:slug>/', views.rate, name='rate'),
    path('talent_zoom', views.talent_zoom, name='talent_zoom'),
    path('join-zoom-meeting/<int:zoom_meeting_id>', views.join_zoom_meeting, name='join_zoom_meeting'),
]
