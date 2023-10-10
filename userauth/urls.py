from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_request, name='login'),
    path("register", views.register_request, name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name="activate"),
    path('check-email/', views.CheckEmailView.as_view(), name="check_email"),
    path('success/', views.SuccessView.as_view(), name="success"),
    path('auth', views.auth_view, name='auth'),
    # path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
]
