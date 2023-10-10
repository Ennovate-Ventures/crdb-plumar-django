import json
from typing import NoReturn

from django.contrib import messages
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from django.db.models.functions import Length
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from dashboard.models import Package, PackagePayment, Matches
from opportunity.models import Opportunity
from startups.models import Startup
from talents.models import Talent
from userauth.models import Profile
from .forms import MyForm
from .models import Watchlist, PopularSearch, Contact, Project


class HomeView(View):
    form_class = MyForm
    initial = {'key': 'value'}
    template_name = 'home/home1.html'

    @staticmethod
    def get_popular_searched():
        return PopularSearch.objects.annotate(keyword_length=Length('keyword')) \
                   .filter(keyword_length__lt=20)[:13]

    def get(self, request, *args, **kwargs):
        startups = Startup.objects.all().order_by('-id')[:10]
        listings = Package.objects.all()
        talents = Talent.objects.all()
        matches = Matches.objects.all()

        opportunities = Opportunity.objects.filter(expired=False, active=True).order_by('-id')

        startup = Profile.objects.filter(user_type='startup')[:3]

        category = request.GET.get('category')
        location = request.GET.get('location')

        if category:
            opportunities = Opportunity.objects.filter(
                Q(category__icontains=category) | Q(title__icontains=category), expired=False, active=True).order_by(
                '-id')

        elif location:
            opportunities = Opportunity.objects.filter(
                Q(location__icontains=location), expired=False, active=True).order_by('-id')

        save_popular_searches(category)

        page = request.GET.get('page', 1)
        paginator = Paginator(opportunities, 10)
        try:
            opps = paginator.page(page)
        except PageNotAnInteger:
            opps = paginator.page(1)
        except EmptyPage:
            opps = paginator.page(paginator.num_pages)

        package = None
        if request.user.is_authenticated:
            package = PackagePayment.objects.filter(user=request.user).last()

        context = {
            'opportunities': opportunities,
            'opps': opps,
            'startup': startup,
            'startups': startups,
            'listings': listings,
            'package': package,
            'talents': talents,
            'matches': matches,
            'popular_searches': self.get_popular_searched()

        }

        return render(request, self.template_name, context)


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
        if category:
            search = PopularSearch.objects.get(keyword=category)
            search.search_count += 1
            search.save()


def home(request):
    opportunities = Opportunity.objects.all().order_by('-id')[:9]
    startups = Startup.objects.all().order_by('-id')[:10]
    listings = Package.objects.all()
    talents = Talent.objects.all()
    matches = Matches.objects.all()

    package = ''
    if request.user.is_authenticated:
        package = PackagePayment.objects.filter(user=request.user).last()

    context = {
        'opportunities': opportunities,
        'startups': startups,
        'listings': listings,
        'package': package,
        'talents': talents,
        'matches': matches

    }
    return render(request, 'home/home.html', context)


def watchlist(request):
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        profession = request.POST['prof']
        location = request.POST['location']
        career_background = request.POST['career']
        response_data = {}
        watchlist = Watchlist(full_name=full_name, email=email, profession=profession,
                              location=location, career_background=career_background)
        watchlist.save()
        response_data['success'] = "Information has been succesful submited"
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )

    return redirect('landing')


def about(request):
    return render(request, 'home/about.html')


def contacts(request):
    return render(request, 'home/contacts.html')


def landing(request):
    form = MyForm(initial={'key': 'value'})
    packages = None
    if request.user.is_authenticated:
        packages = PackagePayment.objects.filter(user=request.user).last()

    context = {
        "form": form,
        "packages": packages,
        "package_listings": Package.objects.all(),
    }

    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            company_name=request.POST.get("company"),
            location=request.POST.get("location"),
            profession=request.POST.get("profession"),
            engage_as=request.POST.get("engage_as"),
        )

    return render(request, "landing/index.html", context)


def lms_home(request):
    return render(request, 'home/lms_home.html')


def handler404(request, exception):
    return render(request, 'errors/404.html', locals())


def terms_conditions(request):
    return render(request, 'home/terms_conditions.html')


def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')


def how_it_works(request):
    return render(request, 'home/how_it_works.html')


def post_project(request):
    if request.method == 'POST':
        try:
            Project.objects.create(
                full_name=request.POST.get("full_name"),
                company_name=request.POST.get("company"),
                position=request.POST.get("position"),
                phone_number=request.POST.get("phone"),
                email=request.POST.get("email"),
                country=request.POST.get("country"),
                description=request.POST.get("description"),
                expectations=request.POST.get("expectations"),
                achievement=request.POST.get("achievement"),
                design=request.POST.get("design"),
                mockup=request.POST.get("mockup"),
                delivery_time=request.POST.get("delivery_time"),
                budget=request.POST.get("budget"),
                more_info=request.POST.get("moreinfo"),
            )
            messages.success(request, "Project submitted successfully.")
            return redirect("post_project")
        except Exception as e:
            print(e.__str__())
            messages.error(request, "Something went wrong, try to submit again")

    return render(request, 'home/post_project.html')
