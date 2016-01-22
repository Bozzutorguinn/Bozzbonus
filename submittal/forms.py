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
    stabilization_day = forms.ChoiceField(
        choices=(),
        required=True,
        label='Day'
    )


class EnterOpeningDateForm(forms.Form):
    def __init__(self,
                 year_choices,
                 month_choices,
                 day_choices,
                 *args,
                 **kwargs):
        super(EnterOpeningDateForm, self).__init__(*args, **kwargs)
        self.fields['opening_year'].choices = year_choices
        self.fields['opening_month'].choices = month_choices
        self.fields['opening_day'].choices = day_choices

    opening_year = forms.ChoiceField(
        choices=(),
        required=True,
        label='Year'
    )
    opening_month = forms.ChoiceField(
        choices=(),
        required=True,
        label='Month'
    )
    opening_day = forms.ChoiceField(
        choices=(),
        required=True,
        label='Day'
    )


#use this form to edit any input that requires a percentage between 0% - 100%
class EditRateForm(forms.Form):
    def __init__(self,
                 rate_choices,
                 *args,
                 **kwargs):
        super(EditRateForm, self).__init__(*args, **kwargs)
        self.fields['rate_amount'].choices = rate_choices

    rate_amount = forms.DecimalField(max_digits=4, decimal_places=1, max_value=100.0, min_value=0, required=True, label='% Rate')

#use this form to edit any input that requires a dollar amount
class EditDollarInputForm(forms.Form):
    dollar_amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=True, label='$ Amount')

#use this form to edit any input that requires a quantity to be entered, such as the number of bad debt write-offs
class EditQuantityForm(forms.Form):
    quantity_amt = forms.IntegerField(min_value=0, required=True, label='# Quantity')

#use this form to edit any input that requires a yes/no response
class EditYesNoForm(forms.Form):
    def __init__(self,
                 yes_no_choices,
                 *args,
                 **kwargs):
        super(EditYesNoForm, self).__init__(*args, **kwargs)
        self.fields['yes_no_select'].choices = yes_no_choices

    yes_no_select = forms.ChoiceField(
        choices=(),
        required=True,
        label='Yes/No'
    )