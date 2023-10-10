import json
from typing import NoReturn

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from dashboard.models import Matches
from home.models import PopularSearch
from talents.models import Talent
from userauth.models import Profile
from .models import Opportunity


# Create your views here.


def opportunity(request):
    opportunities = Opportunity.objects.filter(active=True, expired=False).order_by('-id')
    opportunities_count = opportunities.count()

    startup = Profile.objects.filter(user_type='startup')[:3]

    category = request.GET.get('category')
    location = request.GET.get('location')

    if category:
        opportunities = Opportunity.objects.filter(
            Q(category__icontains=category) | Q(title__icontains=category), active=True, expired=False).order_by('-id')

    elif location:
        opportunities = Opportunity.objects.filter(
            Q(location__icontains=location), active=True, expired=False).order_by('-id')

    save_popular_searches(category)

    page = request.GET.get('page', 1)
    paginator = Paginator(opportunities, 10)
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)

    context = {
        'opportunities': opportunities,
        'opportunities_count': opportunities_count,
        'opps': opps,
        'startup': startup,
    }

    return render(request, 'opportunity/opportunity.html', context)


def save_popular_searches(category) -> NoReturn:
    try:
        split_category = category.split(" ")
        sub_string_found = False
        for _ in split_category:
            qs = PopularSearch.objects.filter(Q(keyword__icontains=_) and Q(keyword__icontains=category))
            if qs:
                sub_string_found = True
                for q in qs:
                    q.search.search_count += 1
                    q.search.save()
        if not sub_string_found:
            PopularSearch.objects.create(keyword=category)
    except Exception as e:
        print(e)
        if category:
            search = PopularSearch.objects.get(keyword=category)
            search.search_count += 1
            search.save()


def opportunity_details(request, id):
    opportunity = Opportunity.objects.get(id=id)
    all_opportunities = Opportunity.objects.all().order_by('-id')[:5]
    opportunities = Opportunity.objects.filter(user=opportunity.user).order_by('-id')[:4]

    matched = False
    # Everything here was done wrong, from a bad project design
    # So I had to fix things on the fly to meet the deadline
    if request.user.profile.user_type == "talent":
        talent = request.user.talent_set.first()
        matches = Matches.objects.filter(user=request.user, talent=talent)
        if matches:
            for match in matches:
                if opportunity in match.opportunity.all():
                    matched = True

    context = {
        'data': opportunity,
        'opportunities': opportunities,
        'all': all_opportunities,
        'matched': matched,
    }

    return render(request, 'opportunity/opportunity_details.html', context)


def add_match(request):
    talent = Talent.objects.get(user=request.user)
    if request.method == 'POST':
        startup = request.POST.get('the_startup')
        opportunity = Opportunity.objects.get(id=int(request.POST.get('the_opp')))
        response_data = {}
        matched = Matches.objects.filter(user=request.user, opportunity=opportunity)
        if matched.exists():
            response_data['result'] = "You have already matched this opportunity."
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json")
        else:
            matches = Matches(startup_id=startup, user=request.user, talent=talent)
            matches.save()
            matches.opportunity.add(opportunity)

            opportunity.matched += 1
            opportunity.save()

            response_data['result'] = "Match submited"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({'Error': 'Failed to submit'}),
            content_type="application/json"
        )


def remove_match(request, id):
    match = Matches.objects.get(id=id)
    match.delete()
    messages.success(request, 'Successful Deleted your match')
    return redirect('talent_dash')


def mark(request):
    if request.method == 'POST':
        opp = Opportunity.objects.get(id=request.POST.get('id'))
        is_marked = False
        if opp.marked.filter(id=request.user.id).exists():
            opp.marked.remove(request.user)
            is_marked = False
        else:
            opp.marked.add(request.user)
            is_marked = True

        response_data = {}
        response_data['result'] = 'Successfull marked'
        response_data['is_marked'] = is_marked
        response_data['the_id'] = opp.id
        return HttpResponse(
            json.dumps(response_data),
            content_type='applicatin/json'
        )
    else:
        return HttpResponse(
            json.dumps({'Error': 'Faild to submit'}),
            content_type="application/json"
        )
