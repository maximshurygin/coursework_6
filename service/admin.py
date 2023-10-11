from django.contrib import admin

from service.models import Client, Newsletter, Message


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment',)
    search_fields = ('email', 'full_name',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('message', 'recipients_list', 'start_time', 'end_time', 'periodicity', 'status',)
    list_filter = ('status',)

    def recipients_list(self, obj):
        return ", ".join([client.full_name for client in obj.recipients.all()])

    recipients_list.short_description = 'Получатели рассылки'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body',)
    search_fields = ('subject', 'body',)
