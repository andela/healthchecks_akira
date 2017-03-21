from django import forms
from django.utils import timezone

from hc.api.models import Channel, Post


class NameTagsForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=500, required=False)

    def clean_tags(self):
        l = []

        for part in self.cleaned_data["tags"].split(" "):
            part = part.strip()
            if part != "":
                l.append(part)

        return " ".join(l)


class TimeoutForm(forms.Form):
    timeout = forms.IntegerField(min_value=60, max_value=7776000)
    grace = forms.IntegerField(min_value=60, max_value=7776000)


class AddChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['kind', 'value']

    def clean_value(self):
        value = self.cleaned_data["value"]
        return value.strip()


class AddWebhookForm(forms.Form):
    error_css_class = "has-error"

    value_down = forms.URLField(max_length=1000, required=False)
    value_up = forms.URLField(max_length=1000, required=False)

    def get_value(self):
        return "{value_down}\n{value_up}".format(**self.cleaned_data)


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def clean_tags(self):
        l = []

        for part in self.cleaned_data["tags"].split(" "):
            part = part.strip()
            if part != "":
                l.append(part)

        return " ".join(l)


# class AddPostForm(forms.Form):
    # STATUS_CHOICES = (
    #     ('draft', 'Draft'),
    #     ('published', 'Published'),
    # )
    # title = forms.CharField(max_length=250)
    # slug = forms.SlugField(max_length=250)
    # author = forms.CharField(max_length=10)
    # body = forms.Textarea()
    # publish = forms.DateTimeField()
    # created = forms.DateTimeField()
    # updated = forms.DateTimeField()
    # status = forms.CharField(max_length=10, choices=STATUS_CHOICES)
    # tags = forms.CharField(max_length=500)

    # def clean_tags(self):
    #     l = []

    #     for part in self.cleaned_data["tags"].split(" "):
    #         part = part.strip()
    #         if part != "":
    #             l.append(part)

    #     return " ".join(l)
