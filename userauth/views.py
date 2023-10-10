from django.contrib import messages
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import RedirectView, TemplateView

from dashboard.models import PackagePayment
from startups.models import Startup
from talents.models import Talent
from .forms import NewUserForm
from .tokens import token_generator
from .utils import email_sender


def auth_view(request):
    return render(request, 'auth/login.html')


def register_request(request):
    if request.method == "POST":
        with transaction.atomic(savepoint=True):
            form = NewUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already taken')
                    return redirect('register')
                else:
                    user = form.save()
                    user.is_active = True
                    user.save()
                    profile = user.profile
                    profile.user_type = form.cleaned_data.get("user_type")
                    profile.save()
                    if profile.user_type == "talent":
                        Talent.objects.create(user=user)
                    else:
                        startup = Startup.objects.create(user=user)
                        PackagePayment.objects.create(startup=startup, user=user, opportunities_to_post=0,
                                                      active_payment=True,
                                                      auto_created=True)

                    user.backend = 'django.contrib.auth.backends.ModelBackend'

                    messages.success(request, "Account created, you can now login")

                # We need the user object, so it's an additional parameter
                # current_site = get_current_site(request)

                # link = f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/" \
                #        f"{token_generator.make_token(user)}/"

                # message = f"Hello {user.username}\n\nWe noticed you just signed up on our website." \
                #           f"\nPlease confirm your email address and activate your account by using the " \
                #           f"link below.\n\n{link}"

                # email_sender.delay(email, "Confirm Email Address", message)
                # send_email.apply_async(args=[email, message])
                # return redirect("check_email")
                return redirect("login")
            else:
                messages.error(request, form.errors)

    return render(request, 'auth/register.html')


class ActivateView(RedirectView):
    url = reverse_lazy('success')

    # Custom get method
    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)

            return super().get(request, uidb64, token)
        else:
            return render(request, 'auth/activate_account_invalid.html')


class CheckEmailView(TemplateView):
    template_name = 'auth/check_email.html'


class SuccessView(TemplateView):
    template_name = 'auth/success.html'


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if not user.is_active:
                messages.error(request, "Account not activated. Use link sent to your email to activate your account")
                return redirect('auth')
            if user is not None:
                login(request, user)
                if request.user.profile.user_type == 'not_set':
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("home")
                elif request.user.profile.user_type == 'startup':
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('dash')
                elif request.user.profile.user_type == 'talent':
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('talent_dash')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('auth')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('auth')
    return render(request, 'auth/login.html')


def logout_request(request):
    logout(request)
    messages.info(request, f"Logged out successful")
    return redirect('home')
