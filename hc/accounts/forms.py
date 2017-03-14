from django import forms
from hc.api.models import Check


class LowercaseEmailField(forms.EmailField):

    def clean(self, value):
        value = super(LowercaseEmailField, self).clean(value)
        return value.lower()


class EmailPasswordForm(forms.Form):
    email = LowercaseEmailField()
    password = forms.CharField(required=False)


class ReportSettingsForm(forms.Form):
    reports_allowed = forms.BooleanField(required=False)


class SetPasswordForm(forms.Form):
    password = forms.CharField()


class InviteTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class RemoveTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class TeamNameForm(forms.Form):
    team_name = forms.CharField(max_length=200, required=True)


class TeamAccessForm(forms.Form):
    user_id = None
    user_check = Check.objects.filter(user=user_id)
    checks = forms.MultipleChoiceField(choices=user_check,
                                       widget=forms.CheckboxSelectMultiple()
                                       )
    member_id = forms.IntegerField()
