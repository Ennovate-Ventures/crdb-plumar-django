from django.urls import path
from . import views

urlpatterns = [
    path('startups', views.startups, name='startups'),
    path('startup/<int:id>', views.startup_details, name='startup_details'),
    path('follow', views.follow, name='follow'),
    path('rate-startup/<int:id>/', views.rate, name='rate_startup'),
    path('create-zoom-meeting', views.create_zoom_meeting, name='create_zoom_meeting'),
    path('delete-zoom-meeting/<int:zoom_meeting_id>', views.delete_zoom_meeting, name='delete_zoom_meeting'),
    path('launch-zoom-meeting/<int:zoom_meeting_id>', views.launch_zoom_meeting, name='launch_zoom_meeting'),
]
