from django import forms

from service.models import Client, Message, Newsletter


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'body',)


class NewsletterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NewsletterForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['recipients'].queryset = Client.objects.filter(owner=user)
            self.fields['message'].queryset = Message.objects.filter(owner=user)

    class Meta:
        model = Newsletter
        fields = ('recipients', 'message', 'start_time', 'end_time', 'periodicity', 'status',)
