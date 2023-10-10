from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from startups.models import ZoomMeeting
from .models import *
from dashboard.models import Rating
from .forms import ratingForm
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin


# Create your views here.

def talents(request):
    talents = Talent.objects.all().order_by('-id')
    talents_count = talents.count()

    qs = request.GET.get('q')
    if qs:
        talents = Talent.objects.filter(
            Q(category__icontains=qs) |
            Q(years_of_experience__icontains=qs) |
            Q(salary_expectation__icontains=qs) |
            Q(prefered_work_type__icontains=qs) |
            Q(gender__icontains=qs) |
            Q(location__icontains=qs) |
            Q(profession__icontains=qs)).order_by('-id')

    page = request.GET.get('page', 1)
    paginator = Paginator(talents, 8)
    try:
        talent = paginator.page(page)
    except PageNotAnInteger:
        talent = paginator.page(1)
    except EmptyPage:
        talent = paginator.page(paginator.num_pages)
    context = {
        'talents': talents,
        'talents_count': talents_count,
        'talent': talent
    }
    return render(request, 'talents/talents.html', context)


def talent_details(request, slug):
    talents = Talent.objects.all().order_by('-id')[:3]
    talent = get_object_or_404(Talent, slug=slug)

    # rating starts
    rating = Rating.objects.filter(rating_for=talent.id)
    sum_of_user_rates = sum(rating.values_list('rating_value', flat=True))  # --> rating for one user filtered above

    all_ratings_to_talent = rating.count() * 5  # --> getting number of all ratings for a filtered user
    try:
        rates = round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
    except ZeroDivisionError:
        rates = 0

    context = {
        'data': talent,
        "talents": talents,
        'rates': rates,
        'rating': rating.order_by('-id')
    }

    hit_count = get_hitcount_model().objects.get_for_object(talent)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    return render(request, 'talents/details.html', context)


def rate(request, slug):
    if request.method == 'POST':
        form = ratingForm(request.POST or None)
        print(request.POST)
        rating = Rating()
        if form.is_valid():
            rating.rating_by = request.user
            rating.rating_for_id = form.cleaned_data['rating_for']
            rating.rating_value = form.cleaned_data['ratings']
            rating.comments = form.cleaned_data['comments']
            rating.save()
            return redirect('talent_details', slug=slug)
        # return redirect('/')

    return redirect('talent_details', slug=slug)


def talent_zoom(request):
    context = {
        "meetings": ZoomMeeting.objects.filter(
            interviewee=request.user.talent_set.first()
        )
    }

    return render(request, 'talent_dash/talent_zoom.html', context)


def join_zoom_meeting(request, zoom_meeting_id):
    if request.method == "POST":
        zoom_meeting = ZoomMeeting.objects.get(id=int(zoom_meeting_id))
        zoom_meeting.interviewee_attended = True
        if zoom_meeting.interviewer_attended:
            zoom_meeting.status = "attended"

            # also change the match status
            try:
                match = zoom_meeting.match
                match.status = "interviewed"
                match.save()
            except AttributeError:
                pass

        zoom_meeting.save()

        messages.success(request, f"You have successfully joined the meeting {zoom_meeting.meeting_id}")

        return redirect(zoom_meeting.join_url)
