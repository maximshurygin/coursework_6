import random
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from users.forms import UserRegisterForm, UserProfileForm, RecoveryForm, \
    VerifyCodeForm
from users.models import User


# Create your views here.

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    if request.method == 'POST':
        form = RecoveryForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                new_password = ''.join([str(random.randint(0, 9))
                                        for _ in range(12)])
                send_mail(
                    subject='Вы сменили пароль',
                    message=f'Ваш новый пароль: {new_password}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email]
                )
                user.set_password(new_password)
                user.save()
                return redirect(reverse('users:login'))
            except ObjectDoesNotExist:
                form.add_error('email', 'Пользователь с таким email не найден')
    else:
        form = RecoveryForm()

    return render(request, 'users/recovery.html', {'form': form})


def verify_code(request):
    if request.method == "POST":
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            user_code = request.POST.get('code')
            if str(user_code) == str(request.user.code):
                request.user.is_verified = True
                request.user.save()
                messages.success(request, 'Ваша почта успешно верифицирована!')
                return redirect('users:profile')
            else:
                messages.error(request, 'Неверный код.')
    else:
        form = VerifyCodeForm()

    return render(request, 'users/verify_code.html', {'form': form})


def send_verification_code(request):
    if request.user.is_authenticated and not request.user.is_verified:
        code = random.randint(1000, 9999)
        request.user.code = code
        request.user.save()
        send_mail(
            subject='Верификация почты',
            message=str(code),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email]
        )
        messages.success(request, 'Код верификации отправлен на вашу почту.')
        return redirect('users:verify_code')
    return redirect('users:profile')


class ToggleUserActiveStatusView(LoginRequiredMixin, PermissionRequiredMixin,
                                 View):
    permission_required = 'users.can_toggle_active'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        user.is_active = not user.is_active
        user.save()
        return redirect('users:user_list')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
