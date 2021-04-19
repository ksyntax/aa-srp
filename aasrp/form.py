"""
Form definitions
"""

import re

from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from aasrp.models import AaSrpLink, AaSrpRequest, AaSrpUserSettings


def get_mandatory_form_label_text(text: str) -> str:
    """
    label text for mandatory form fields
    :param text:
    :type text:
    :return:
    :rtype:
    """

    required_text = _("This field is mandatory")
    required_marker = (
        f'<span aria-label="{required_text}" class="form-required-marker">*</span>'
    )

    return mark_safe(
        f'<span class="form-field-required">{text} {required_marker}</span>'
    )


class AaSrpLinkForm(ModelForm):
    """
    new SRP lnk form
    """

    srp_name = forms.CharField(
        required=True, label=get_mandatory_form_label_text(_("Fleet Name"))
    )
    fleet_time = forms.DateTimeField(
        required=True, label=get_mandatory_form_label_text(_("Fleet Time"))
    )
    fleet_doctrine = forms.CharField(
        required=True, label=get_mandatory_form_label_text(_("Fleet Doctrine"))
    )
    aar_link = forms.CharField(required=False, label=_("AAR Link"))

    class Meta:  # pylint: disable=too-few-public-methods
        """
        meta definitions
        """

        model = AaSrpLink
        fields = ["srp_name", "fleet_time", "fleet_doctrine", "aar_link"]


class AaSrpLinkUpdateForm(ModelForm):
    """
    edit SRP link form
    """

    aar_link = forms.CharField(required=False, label=_("After Action Report Link"))

    class Meta:  # pylint: disable=too-few-public-methods
        """
        meta definitions
        """

        model = AaSrpLink
        fields = ["aar_link"]


# class AaSrpRequestForm(forms.Form):
class AaSrpRequestForm(ModelForm):
    """
    srp request form
    """

    killboard_link = forms.URLField(
        label=get_mandatory_form_label_text(_("zKillboard Link")),
        max_length=254,
        required=True,
        help_text=(
            "Find your kill mail on https://zkillboard.com " "and paste the link here."
        ),
    )

    additional_info = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 20, "input_type": "textarea"}),
        required=True,
        label=get_mandatory_form_label_text(_("Additional Info")),
        help_text=(
            "Please tell us about the circumstances of your untimely demise. "
            "Who was the FC, what doctrine was called, have changes to the fit "
            "been requested and so on. Be as detailed as you can."
        ),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        meta definitions
        """

        model = AaSrpRequest
        fields = ["killboard_link", "additional_info"]

    def clean_killboard_link(self):
        """
        check if it's a zkillboard link and clean it
        :return:
        """

        killboard_link = self.cleaned_data["killboard_link"]

        # check if it's a zkillboard link
        if "zkillboard.com" not in killboard_link:
            raise forms.ValidationError(
                _("Invalid Link. Please use https://zkillboard.com")
            )

        # check if it's an actual kill mail
        if not re.match(r"http[s]?://zkillboard\.com/kill/\d+\/", killboard_link):
            raise forms.ValidationError(
                _("Invalid Link. Please post a link to a kill mail.")
            )

        # check if there is already a SRP request for this killmail
        if AaSrpRequest.objects.filter(killboard_link=killboard_link).exists():
            raise forms.ValidationError(
                _(
                    "There is already a SRP request for this killmail. "
                    "Please check if you got the right one."
                )
            )

        return killboard_link


class AaSrpRequestPayoutForm(forms.Form):
    """
    change payout value
    """

    value = forms.CharField(label=_("SRP payout value"), max_length=254, required=True)


class AaSrpRequestRejectForm(forms.Form):
    """
    SRP request reject form
    """

    reject_info = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 20, "input_type": "textarea"}),
        required=True,
        label=get_mandatory_form_label_text(_("Rejection Reason")),
        help_text=_("Please provide the reason why this SRP request is rejected."),
    )


class AaSrpUserSettingsForm(ModelForm):
    """
    user settings form
    """

    disable_notifications = forms.BooleanField(
        initial=False,
        required=False,
        label=_(
            "Disable notifications. "
            "(Auth and Discord, if a relevant module is installed)"
        ),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        meta definitions
        """

        model = AaSrpUserSettings
        fields = ["disable_notifications"]
