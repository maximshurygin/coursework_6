import random
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from blog.models import Post
from .forms import ClientForm, NewsletterForm, MessageForm
from .models import Client, Newsletter, Message, Log


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client_list')

    def test_func(self):
        return not self.request.user.groups.filter(name='Managers').exists()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                       UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'service.change_client'
    success_url = reverse_lazy('client_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class NewsletterCreateView(LoginRequiredMixin, UserPassesTestMixin,
                           CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_list')

    def test_func(self):
        return not self.request.user.groups.filter(name='Managers').exists()

    def get_form_kwargs(self):
        kwargs = super(NewsletterCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messages_list')

    def test_func(self):
        return not self.request.user.groups.filter(name='Managers').exists()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messages_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('messages_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    template_name = 'service/log_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(newsletter__owner=self.request.user)


class ToggleNewsletterStatusView(LoginRequiredMixin, PermissionRequiredMixin,
                                 View):
    permission_required = 'service.can_toggle_active'

    def get(self, request, *args, **kwargs):
        newsletter = get_object_or_404(Newsletter, pk=kwargs.get('pk'))
        newsletter.is_active = not newsletter.is_active
        if not newsletter.is_active:
            newsletter.status = 'completed'
        newsletter.save()
        return redirect('newsletter_list')


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        newsletters_count = cache.get('newsletters_count')
        if newsletters_count is None:
            newsletters_count = Newsletter.objects.count()
            cache.set('newsletters_count', newsletters_count, 60 * 15)

        active_newsletters_count = cache.get('active_newsletters_count')
        if active_newsletters_count is None:
            active_newsletters_count = Newsletter.objects. \
                filter(is_active=True). \
                exclude(status='completed').count()
            cache.set('active_newsletters_count',
                      active_newsletters_count, 60 * 15)

        unique_clients_count = cache.get('unique_clients_count')
        if unique_clients_count is None:
            unique_clients_count = Client.objects.values('email'). \
                distinct().count()
            cache.set('unique_clients_count', unique_clients_count, 60 * 15)

        all_posts_ids = Post.objects.values_list('id', flat=True)
        random_ids = random.sample(list(all_posts_ids),
                                   min(len(all_posts_ids), 3))
        random_posts = Post.objects.filter(id__in=random_ids)

        context = {
            'newsletters_count': newsletters_count,
            'active_newsletters_count': active_newsletters_count,
            'unique_clients_count': unique_clients_count,
            'random_posts': random_posts,
        }
        return render(request, 'service/home.html', context)
