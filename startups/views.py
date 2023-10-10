import json

import requests
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from dashboard.models import Matches
from sandbox import settings
from talents.models import Talent
from .models import Startup, Startup_Rating, ZoomMeeting
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from .forms import ratingForm


def startups(request):
    startups_qs = Startup.objects.all().order_by('-id')
    startup_count = startups_qs.count()

    qs = request.GET.get('q')
    if qs:
        startups_qs = Startup.objects.filter(
            Q(name__icontains=qs) |
            Q(size__icontains=qs) |
            Q(location__icontains=qs) |
            Q(description__icontains=qs) |
            Q(category__icontains=qs)).order_by('-id')

    page = request.GET.get('page', 1)
    paginator = Paginator(startups_qs, 8)
    try:
        startup = paginator.page(page)
    except PageNotAnInteger:
        startup = paginator.page(1)
    except EmptyPage:
        startup = paginator.page(paginator.num_pages)
    context = {
        'startups': startups_qs,
        'startup': startup,
        'startup_count': startup_count,

    }
    return render(request, 'startups/startups.html', context)


def startup_details(request, id):
    startup = get_object_or_404(Startup, id=id)

    rating = Startup_Rating.objects.filter(rating_for=startup.id)
    sum_of_user_rates = sum(rating.values_list('rating_value', flat=True))  # --> rating for one user filtered above

    all_ratings_to_talent = rating.count() * 5  # --> getting number of all ratings for a filtered user
    try:
        rates = round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
    except ZeroDivisionError:
        rates = 0

    context = {
        'data': startup,
        'rates': rates
    }

    hit_count = get_hitcount_model().objects.get_for_object(startup)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    return render(request, 'startups/startupDetails.html', context)


def follow(request):
    if request.method == 'POST':
        startup = get_object_or_404(Startup, id=request.POST.get('id'))
        is_followed = False
        if startup.followers.filter(id=request.user.id).exists():
            startup.followers.remove(request.user)
            is_followed = False
        else:
            startup.followers.add(request.user)
            is_followed = True

        followers_count = startup.followers.all().count()
        response_data = {}
        response_data['result'] = 'Successfully followed'
        response_data['is_followed'] = is_followed
        response_data['the_id'] = startup.id
        response_data['count'] = followers_count
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps({'Error': 'Failed to submit'}),
            content_type="application/json"
        )


def rate(request, id):
    if request.method == 'POST':
        form = ratingForm(request.POST or None)
        print(request.POST)
        rating = Startup_Rating()
        if form.is_valid():
            rating.rating_by = request.user
            rating.rating_for_id = form.cleaned_data['rating_for']
            rating.rating_value = form.cleaned_data['ratings']
            rating.comments = form.cleaned_data['comments']
            rating.save()
            return redirect('startup_details', id=id)
        # return redirect('/')

    return redirect('startup_details', id=id)

    # CRO-IUdq-I5Dl-VuQ9h


def create_zoom_meeting(request):
    if request.method == 'POST':
        payload = {
            'agenda': request.POST.get("agenda"),
            'default_password': False,
            'duration': 60,
            'password': request.POST.get("password"),
            'pre_schedule': False,
            'start_time': request.POST.get("start_time"),
            'allow_multiple_devices': True,
            'auto_recording': 'cloud',
            'contact_name': request.POST.get("contact_name"),
            'contact_email': request.POST.get("host_email"),
            'email_notification': True,
            'join_before_host': False,
            'timezone': 'Africa/Nairobi',
            'topic': request.POST.get("agenda"),
            'type': 2,
        }
        headers = {
            'authorization': 'Bearer ' + settings.ZOOM_API_JWT_TOKEN,
            'content-type': 'application/json'
        }
        response = requests.post('https://api.zoom.us/v2/users/me/meetings',
                                 headers=headers, data=json.dumps(payload))

        # print(response.status_code)
        # print(response.text)
        # print(response.reason)
        if response.status_code == 201:
            json_response = json.loads(response.text)
            ZoomMeeting.objects.create(
                meeting_id=json_response.get("id"),
                meeting_uuid=json_response.get("uuid"),
                host_id=json_response.get("host_id"),
                host_email=json_response.get("host_email"),
                status=json_response.get("status"),
                start_time=request.POST.get("start_time"),
                start_url=json_response.get("start_url"),
                join_url=json_response.get("join_url"),
                agenda=json_response.get("agenda"),
                default_password=True,
                duration=json_response.get("duration"),
                encrypted_password=json_response.get("encrypted_password"),
                password=json_response.get("password"),
                pre_schedule=json_response.get("pre_schedule"),
                allow_multiple_devices=json_response.get("settings").get("allow_multiple_devices"),
                auto_recording=False,
                contact_name=request.POST.get("contact_name"),
                contact_email=request.POST.get("contact_email"),
                timezone=json_response.get("timezone"),
                topic=json_response.get("topic"),
                interviewer=request.user.startup_set.first(),
                interviewee=Talent.objects.get(id=int(request.POST.get("talent_id"))),
                match=Matches.objects.get(id=int(request.POST.get("match_id"))),
            )

        if response.status_code == 201:
            messages.success(request, "Meeting created successfully")
            return redirect("matches")
        else:
            messages.error(request, "Something went wrong, try again")
            return redirect("matches")


def delete_zoom_meeting(request, zoom_meeting_id):
    if request.method == "POST":
        headers = {
            'authorization': 'Bearer ' + settings.ZOOM_API_JWT_TOKEN,
            'content-type': 'application/json'
        }
        response = requests.delete(f'https://api.zoom.us/v2/users/me/meetings/{zoom_meeting_id}', headers=headers)

        print(response.status_code)
        print(response.text)

        if response.status_code == 200:
            messages.success(request, "Meeting deleted successfully")
            ZoomMeeting.objects.get(meeting_id=zoom_meeting_id).delete()

        return HttpResponse(status=response.status_code)


@csrf_exempt
def launch_zoom_meeting(request, zoom_meeting_id):
    if request.method == "POST":
        zoom_meeting = ZoomMeeting.objects.get(id=int(zoom_meeting_id))
        zoom_meeting.interviewer_attended = True
        if zoom_meeting.interviewee_attended:
            zoom_meeting.status = "attended"
        zoom_meeting.save()

        messages.success(request, f"You have successfully launched the meeting {zoom_meeting.meeting_id}")
        return HttpResponse(status=200)
