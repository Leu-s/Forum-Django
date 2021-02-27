from django.urls import reverse
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import AdvancedUser

from .forms import UserPersonalInformationForm
from .forms import UserRegistrationForm

from .utilities import signer
from .utilities import send_activation_notification


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
    form_class = UserPersonalInformationForm

    def get_success_url(self):
        user = AdvancedUser.objects.get(email=self.request.POST.get('email'))
        if user:
            return reverse_lazy('main:user_personal_info', kwargs={'slug': user.slug})
        else:
            return reverse_lazy('main:main_page')


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


def user_activation(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        messages.add_message(
            request=request,
            level=messages.ERROR,
            message='Виникла помилка, адрес підтвердження не вірний!'
        )
        return reverse_lazy('main:main_page')
    user = get_object_or_404(AdvancedUser, username=username)

    if user.is_activated:
        messages.add_message(
            request=request,
            level=messages.WARNING,
            message=f'Користувач {user.username} був активований раніше.'
        )
        return HttpResponseRedirect(reverse_lazy('main:main_page'))
    else:
        messages.add_message(
            request=request,
            level=messages.SUCCESS,
            message=f'Вітаємо Вас, {username}. Ви успішно активувалі свій профіль!'
        )
        user.is_activated = True
        user.save()
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main:user_personal_info', kwargs={'slug': user.slug}))
        else:
            return HttpResponseRedirect(reverse_lazy('main:user_login'))


@login_required()
def user_profile(request, slug):
    template = 'account/user_profile.html'
    if request.method == 'POST':
        if 'send_email' in request.POST:
            messages.add_message(
                request=request,
                level=messages.SUCCESS,
                message='Лист з даними для підтвердження профілю було відправлено.'
            )
            user = AdvancedUser.objects.get(username=request.user.username)
            send_activation_notification(user=user)
    context = {
        'slug': slug
    }
    return render(request, template, context)










