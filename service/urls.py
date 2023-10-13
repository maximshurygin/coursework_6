from django.urls import path
from service.views import HomePageView, NewsletterListView, \
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    NewsletterDetailView, NewsletterCreateView, ClientDetailView, \
    NewsletterUpdateView, NewsletterDeleteView, MessageListView, \
    MessageUpdateView, MessageDetailView, MessageCreateView, \
    MessageDeleteView, LogListView, ToggleNewsletterStatusView

urlpatterns = [

    path('', HomePageView.as_view(),
         name='home'),

    path('newsletters', NewsletterListView.as_view(),
         name='index'),

    path('clients/', ClientListView.as_view(),
         name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(),
         name='client_detail'),
    path('clients/add/', ClientCreateView.as_view(),
         name='client_add'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(),
         name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(),
         name='client_delete'),

    path('newsletters/', NewsletterListView.as_view(),
         name='newsletter_list'),
    path('newsletters/<int:pk>/', NewsletterDetailView.as_view(),
         name='newsletter_detail'),
    path('newsletters/add/', NewsletterCreateView.as_view(),
         name='newsletter_add'),
    path('newsletters/<int:pk>/edit/', NewsletterUpdateView.as_view(),
         name='newsletter_edit'),
    path('newsletters/<int:pk>/delete/', NewsletterDeleteView.as_view(),
         name='newsletter_delete'),
    path('newsletter/<int:pk>/update_status/',
         ToggleNewsletterStatusView.as_view(),
         name='update_newsletter_status'),

    path('messages/', MessageListView.as_view(),
         name='messages_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(),
         name='messages_detail'),
    path('messages/add/', MessageCreateView.as_view(),
         name='messages_add'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(),
         name='messages_edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(),
         name='messages_delete'),

    path('logs/', LogListView.as_view(), name='log_list'),
]
