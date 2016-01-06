from django import forms


class EditLeasingStatusForm(forms.Form):
    def __init__(self,
                 leasing_status_choices,
                 *args,
                 **kwargs):
        super(EditLeasingStatusForm, self).__init__(*args, **kwargs)
        self.fields['leasing_status'].choices = leasing_status_choices

    leasing_status = forms.ChoiceField(
        choices=(),
        required=True,
        label='Leasing Status'
    )


class EnterStabilizationDateForm(forms.Form):
    def __init__(self,
                 year_choices,
                 month_choices,
                 day_choices,
                 *args,
                 **kwargs):
        super(EnterStabilizationDateForm, self).__init__(*args, **kwargs)
        self.fields['stabilization_year'].choices = year_choices
        self.fields['stabilization_month'].choices = month_choices
        self.fields['stabilization_day'].choices = day_choices

    stabilization_year = forms.ChoiceField(
        choices=(),
        required=True,
        label='Year'
    )
    stabilization_month = forms.ChoiceField(
        choices=(),
        required=True,
        label='Month'
    )
    stabilization_year = forms.ChoiceField(
        choices=(),
        required=True,
        label='Day'
    )