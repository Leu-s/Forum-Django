from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import AdvancedUser

from .forms import UserPersonalInformationForm

def main_page(request):
    return render(request, 'articles/main_page.html')


class UserLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('main:main_page')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('main:main_page')


class UserPersonalInformationView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvancedUser
    template_name = 'account/user_personal_information.html'
    success_message = 'Ваша персональна інформація збережена'
    success_url = reverse_lazy('main:main_page')
    form_class = UserPersonalInformationForm

