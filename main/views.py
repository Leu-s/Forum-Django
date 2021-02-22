from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import AdvancedUser

from .forms import UserPersonalInformationForm
from .forms import UserRegistrationForm


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


def user_registration(request):
    template = 'account/user_registration.html'
    form = UserRegistrationForm
    if request.method == 'POST':
        new_user = UserRegistrationForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            # в этом месте отправляем письмо для подтверждения эл.почты
            messages.add_message(
                request,
                level=messages.SUCCESS,
                message=f'Вітаємо, {request.POST["username"]}.'
                        f'Реєстрація пройшла успішно. На вашу електронну адресу відправлений'
                        f'лист з інструкцією для активації аккаута.')
            return HttpResponseRedirect(reverse_lazy('main:user_login'))
        else:
            context = {'form': new_user}
            return render(request, template_name=template, context=context)
    return render(request, template_name=template, context={'form': form})









