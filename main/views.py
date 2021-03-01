from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetConfirmView
from django.views.generic import TemplateView
from django.core.signing import BadSignature
from django.db.models import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import EnterOldPasswordForm
from .forms import FirstPersonalInformationForm
from .forms import SecondPersonalInformationForm
from .forms import UserRegistrationForm
from .models import AdvancedUser
from .models import ChangesInUserInformation
from .utilities import send_activation_notification
from .utilities import send_confirmation_to_update_personal_information
from .utilities import send_request_to_change_password
from .utilities import signer


def main_page(request):
    return render(request, 'articles/main_page.html')


class UserLoginView(LoginView):
    """Страница авторизации пользователя"""
    template_name = 'account/login.html'
    success_url = reverse_lazy('main:main_page')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    """Выход из аккаунта"""
    next_page = reverse_lazy('main:main_page')


class UserPersonalInformationView(LoginRequiredMixin, TemplateView):
    template_name = 'account/user_personal_information.html'

    def get_context_data(self, **kwargs):
        user = get_object_or_404(AdvancedUser, username=self.request.user.username)
        initial_first_form = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number
        }
        initial_second_form = {
            'user_image': user.user_image,
            'village': user.village,
            'date_of_birth': user.date_of_birth,
            'about_me': user.about_me
        }
        first_form = FirstPersonalInformationForm(initial=initial_first_form)
        second_form = SecondPersonalInformationForm(initial=initial_second_form)
        change_password_form = PasswordChangeForm(user=user)
        context = super().get_context_data(**kwargs)
        context['first_form'] = first_form
        context['second_form'] = second_form
        context['password_change_form'] = change_password_form
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(AdvancedUser, username=request.user.username)
        context = self.get_context_data()
        if 'first_form' in request.POST:
            first_form = self._process_the_first_form(user=user)
            context['first_form'] = first_form
        elif 'second_form' in request.POST:
            second_form = self._save_second_form(user=user)
            context['second_form'] = second_form
            return HttpResponseRedirect(reverse_lazy('main:user_personal_info', kwargs={'slug': user.slug}))
        elif 'change_password' in request.POST:
            password_form = self._process_password_change_form(user=user)
            context['password_change_form'] = password_form

        return self.render_to_response(context=context)

    def _save_second_form(self, user):
        """
        The method validates and saves the form with
        additional information about the user.

        :return: form
        """
        form = SecondPersonalInformationForm(data=self.request.POST, files=self.request.FILES, instance=user)
        if form.is_valid():
            messages.add_message(
                request=self.request,
                level=messages.SUCCESS,
                message='Персональну інформацію було оновлено')
            form.save()
        return form

    def _process_the_first_form(self, user):
        """
        The model checks the entered data for correctness (first name, last name, email and phone number),
        and if successful, sends an email to the user to confirm the changes.
        Temporary data is stored in the database.


        :param user: The user model instance that initiated the information change.
        :return: Form
        """
        form = FirstPersonalInformationForm(data=self.request.POST, instance=user)
        if form.is_valid():
            messages.add_message(
                request=self.request,
                level=messages.SUCCESS,
                message=f'На електронну адресу ({self.request.user.email}) відправлений лист для підтвердження.')
            data = form.cleaned_data
            temporary_information = ChangesInUserInformation.objects.get_or_create(user=user)[0]
            temporary_information.new_first_name = data['first_name']
            temporary_information.new_last_name = data['last_name']
            temporary_information.new_email = data['email']
            temporary_information.new_phone_number = data['phone_number']
            temporary_information.save()
            send_confirmation_to_update_personal_information(user=user)
        return form

    def _process_password_change_form(self, user):
        """
        Processing the password change form.

        :param user: The user model instance that initiated the information change.
        :return: form
        """
        form = PasswordChangeForm(user=user, data=self.request.POST)
        if form.is_valid():
            if form.is_valid():
                messages.add_message(
                    request=self.request,
                    level=messages.SUCCESS,
                    message='Ви успішно змінили свій пароль')
                form.save()
        return form


@login_required
def email_confirm_update_personal_information(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        messages.add_message(
            request=request,
            level=messages.ERROR,
            message='Виникла помилка, посилання не вірне.'
        )
        return reverse_lazy('main:main_page')
    user = get_object_or_404(AdvancedUser, username=username)
    new_information = ChangesInUserInformation.objects.get(user=user)
    if new_information:
        user.first_name = new_information.new_first_name
        user.last_name = new_information.new_last_name
        user.email = new_information.new_email
        user.phone_number = new_information.new_phone_number
        user.save()
        new_information.delete()
        messages.add_message(
            request,
            level=messages.SUCCESS,
            message='Персональну інформацію було оновлено')
    else:
        messages.add_message(
            request,
            level=messages.ERROR,
            message="Виникла невідома помилка. Будь-ласка, зв'яжіться з "
                    "адміністрацією сайта для вирішення проблеми, або"
                    "спробуйте відправити лист підтверждення ще раз.")
    return HttpResponseRedirect(reverse_lazy('main:user_personal_info', kwargs={'slug': user.slug}))


def user_registration(request):
    template = 'account/user_registration.html'
    form = UserRegistrationForm
    if request.method == 'POST':
        new_user = UserRegistrationForm(request.POST)
        if new_user.is_valid():
            new_user.save()
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


def user_forgot_his_password(request):
    if request.user.is_authenticated:
        return reverse_lazy('main:user_profile')
    if request.method == 'POST':
        old_email = request.POST.get('old_email')
        if old_email:
            search_user = None
            try:
                search_user = AdvancedUser.objects.get(email__icontains=old_email)
            except ObjectDoesNotExist:
                messages.add_message(
                    request=request,
                    level=messages.ERROR,
                    message='Користувача з такою електронною поштою не знайдено'
                )
                return HttpResponseRedirect(reverse_lazy('main:user_forgot_his_password'))
            send_request_to_change_password(user=search_user)
            messages.add_message(
                request=request,
                level=messages.SUCCESS,
                message='На вашу електронну адресу був відправлений лист з інструкцією.'
            )
        else:
            messages.add_message(
                request=request,
                level=messages.WARNING,
                message="Обов'язково необхідно вказати свою електронну адресу."
            )
            return HttpResponseRedirect(reverse_lazy('main:user_forgot_his_password'))
    template = 'account/user_forgot_password.html'
    context = {'form': EnterOldPasswordForm}
    return render(request, template, context)


class UserResetPasswordView(PasswordResetConfirmView):
    template_name = 'account/user_password_reset.html'
    success_url = reverse_lazy('main:user_login')


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
