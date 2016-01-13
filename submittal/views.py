from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from property.models import Property
from .models import Submittal
from .forms import EditLeasingStatusForm, EnterStabilizationDateForm, EnterOpeningDateForm
from user_access.tools import CheckAuthorization
import datetime

@login_required
def SubmittalDetail(request, submittal_id):
    submittal = Submittal.objects.get(id=submittal_id)
    property_id = submittal.prop_id
    property = Property.objects.get(id=property_id)
    #check that the logged-in user is authorized to view the property
    authorized_user = CheckAuthorization(request, property_id)
    if authorized_user == True:
        #check the submittal status to see whether or not the user can edit the numbers
        submittal_status = CheckSubmissionStatus(submittal_id=submittal_id)
        #check that the property has enetered an opening date
        open_date_complete = CheckOpeningDate(property_id=property_id)
        #check that a stabilization date has been entered if the property is listed as stabilized
        stabilization_date_complete = CheckStabilizationDate(submittal_id=submittal_id)
        print stabilization_date_complete
        #convert the boolean 0/1 for lease-up override to 'yes' or 'no'
        lease_up_override = 'No'
        if submittal.lease_up_override == 1:
            lease_up_override = 'Yes'
        #convert the boolean 0/1 for bad debt writeoff to 'yes' or 'no'
        bad_debt_writeoff = 'No'
        if submittal.bad_debt_writeoffs == 1:
            bad_debt_writeoff = 'Yes'
        #check that the leasing status has been filled out
        leasing_status_confirmed = 'No'
        if submittal.leasing_status == 'stabilized' or submittal.leasing_status == 'leaseup':
            leasing_status_confirmed = 'Yes'
        #check whether or not all of the open data points has been filled out to allow for bonuses to be calculated
        context = {'submittal': submittal,
                   'property': property,
                   'lease_up_override': lease_up_override,
                   'bad_debt_writeoff': bad_debt_writeoff,
                   'leasing_status_confirmed': leasing_status_confirmed,
                   'submittal_status': submittal_status,
                   'open_date_complete': open_date_complete,
                   'stabilization_date_complete': stabilization_date_complete,
                   }
        return render(request, 'submittal/submittal_detail.html', context)

@login_required
def EditLeasingStatus(request, submittal_id):
    submittal = Submittal.objects.get(id=submittal_id)
    property_id = submittal.prop_id
    property = Property.objects.get(id=property_id)
    options = LeasingStatusOptions()
    #check that the user is authorized
    authorized_user = CheckAuthorization(request, property_id)
    if authorized_user == True:
        if request.method == 'POST':
            form = EditLeasingStatusForm(
                data=request.POST,
                leasing_status_choices=options,
            )
            if form.is_valid():
                data = form.cleaned_data
                #check to make sure that they are not changing status from stabilized to leaseup
                prior_period = PriorMonthSubmittalDates(submittal_id=submittal_id)
                prior_year = prior_period['prior_year']
                prior_month = prior_period['prior_month']
                submittal_prior_month = Submittal.objects.filter(prop_id=property_id,
                                                                 submittal_year=prior_year,
                                                                 submittal_month=prior_month)
                leasing_status_prior_month = None
                leasing_status_current_month = data['leasing_status']
                #if the queryset for the prior month submittal comes back empty, it means there wasn't a submittal
                #and that any leasing status now submitted can be saved
                if not submittal_prior_month:
                    submittal.leasing_status = leasing_status_current_month
                    submittal.save()
                    return HttpResponseRedirect(reverse('submittal:submittal_detail', kwargs={'submittal_id': submittal_id}))
                else:
                    leasing_status_prior_month = submittal_prior_month.leasing_status
                    #check that the leasing status is not going from stabilized to leaseup
                    if leasing_status_prior_month == 'stabilized' and leasing_status_current_month == 'leaseup':
                        return render(request, 'submittal/edit_leasing_status.html',{'form': form,
                                                                     'submittal': submittal,
                                                                     'property': property,
                                                                     })
                    #check if the leasing status is going from leaseup to stabilized, and if so,
                    #redirect to a field where they can enter the stabilization date
                    elif leasing_status_prior_month == 'leaseup' and leasing_status_current_month == 'stabilized':
                        submittal.leasing_status = leasing_status_current_month
                        submittal.save()
                        return HttpResponseRedirect(reverse('submittal:edit_stabilization_date', kwargs={'submittal_id': submittal_id}))
                    #if none of the other conditions met, assume no change and the user can save
                    else:
                        submittal.leasing_status = leasing_status_current_month
                        submittal.save()
                        return HttpResponseRedirect(reverse('submittal:submittal_detail', kwargs={'submittal_id': submittal_id}))
        else:
            form = EditLeasingStatusForm(
                leasing_status_choices=options,
                initial={
                    'leasing_status': submittal.leasing_status,
                }
            )
        return render(request, 'submittal/edit_leasing_status.html',{'form': form,
                                                                     'submittal': submittal,
                                                                     'property': property,
                                                                     })
@login_required
def EditStabilizationDate(request, submittal_id):
    submittal = Submittal.objects.get(id=submittal_id)
    property_id = submittal.prop_id
    property = Property.objects.get(id=property_id)
    date_choices = DateChoices()
    authorized_user = CheckAuthorization(request, property_id)
    if authorized_user == True:
        if request.method == 'POST':
            form = EnterStabilizationDateForm(
                data=request.POST,
                year_choices=date_choices['year_choices'],
                month_choices=date_choices['month_choices'],
                day_choices=date_choices['day_choices'],
            )
            if form.is_valid():
                data = form.cleaned_data
                year = data['stabilization_year']
                month = data['stabilization_month']
                day = data['stabilization_day']
                date_check = CheckDates(year=year, month=month, day=day)
                stabilization_date_check = StabilizationOpeningDateCheck(property_id=property_id,
                                                                         stabilization_year=year,
                                                                         stabilization_month=month,
                                                                         stabilization_day=day)
                if (date_check == True) and (stabilization_date_check == True):
                    stabilization_date = datetime.date(year=int(year), month=int(month), day=int(day))
                    property.date_stabilization = stabilization_date
                    property.save()
                    return HttpResponseRedirect(reverse('submittal:submittal_detail', kwargs={'submittal_id': submittal_id}))
                else:
                    message = 'The designated stabilization date is either incorrect or falls before the stabilization date. Try again.'
                    context = {
                        'form': form,
                        'property': property,
                        'submittal': submittal,
                        'message': message,
                    }
                    return render(request, 'submittal/edit_stabilization_date.html', context)
        else:
            form = EnterStabilizationDateForm(
                year_choices=date_choices['year_choices'],
                month_choices=date_choices['month_choices'],
                day_choices=date_choices['day_choices'],
            )
            context = {
                'form': form,
                'property': property,
                'submittal': submittal,
            }
        return render(request, 'submittal/edit_stabilization_date.html', context)

@login_required
def EditOpeningDate(request, submittal_id):
    submittal = Submittal.objects.get(id=submittal_id)
    property_id = submittal.prop_id
    property = Property.objects.get(id=property_id)
    date_choices = DateChoices()
    authorized_user = CheckAuthorization(request, property_id)
    if authorized_user == True:
        if request.method == 'POST':
            form = EnterOpeningDateForm(
                data=request.POST,
                year_choices=date_choices['year_choices'],
                month_choices=date_choices['month_choices'],
                day_choices=date_choices['day_choices']
            )
            if form.is_valid():
                data = form.cleaned_data
                year = data['opening_year']
                month = data['opening_month']
                day = data['opening_day']
                date_check = CheckDates(year=year, month=month, day=day)
                opening_date_check = OpeningStabilizationDateCheck(property_id=property_id,
                                                                         opening_year=year,
                                                                         opening_month=month,
                                                                         opening_day=day)
                if date_check == True and opening_date_check == True:
                    opening_date = datetime.date(year=int(year), month=int(month), day=int(day))
                    property.date_opening = opening_date
                    property.save()
                    return HttpResponseRedirect(reverse('submittal:submittal_detail', kwargs={'submittal_id': submittal_id}))
                else:
                    message = 'The designated opening date is either incorrect or falls after the stabilization date. Try again.'
                    context = {
                        'form': form,
                        'property': property,
                        'submittal': submittal,
                        'message': message,
                    }
                    return render(request, 'submittal/edit_opening_date.html', context)
        else:
            form = EnterOpeningDateForm(
                year_choices=date_choices['year_choices'],
                month_choices=date_choices['month_choices'],
                day_choices=date_choices['day_choices'],
            )
            context = {
                'form': form,
                'property': property,
                'submittal': submittal,
            }
        return render(request, 'submittal/edit_opening_date.html', context)

def LeasingStatusOptions():
    options = []
    options.append(('stabilized', 'stabilized'),)
    options.append(('leaseup', 'leaseup'),)
    return options

def CheckSubmissionStatus(submittal_id):
    submittal = Submittal.objects.get(id=submittal_id)
    submittal_status_boolean = submittal.pm_submitted
    submittal_status = 'open'
    if submittal_status_boolean == 1:
        submittal_status = 'submitted'
    return submittal_status

def CheckOpeningDate(property_id):
    property = Property.objects.get(id=property_id)
    opening_date = property.date_opening
    #in case the database returns an empty value, set the opening date to a dummy date
    if not opening_date or opening_date == None or opening_date == 'null' or opening_date == '':
        opening_date = datetime.date(year=1900, month=1, day=1)
    minimum_date = datetime.date(year=2010, month=1, day=1)
    opening_date_complete = 'incomplete'
    if opening_date >= minimum_date:
        opening_date_complete = 'complete'
    return opening_date_complete

def StabilizationOpeningDateCheck(property_id, stabilization_year, stabilization_month, stabilization_day):
    stabilization_date = datetime.date(year=int(stabilization_year),
                                       month=int(stabilization_month),
                                       day=int(stabilization_day)
                                       )
    stabilization_date_check = False
    property = Property.objects.get(id=property_id)
    opening_date = property.date_opening
    if stabilization_date > opening_date:
        stabilization_date_check = True
    return stabilization_date_check

def OpeningStabilizationDateCheck(property_id, opening_year, opening_month, opening_day):
    opening_date = datetime.date(year=int(opening_year),
                                       month=int(opening_month),
                                       day=int(opening_day)
                                       )
    opening_date_check = False
    property = Property.objects.get(id=property_id)
    stabilization_date = property.date_stabilization
    if not stabilization_date or stabilization_date == '' or stabilization_date == None or stabilization_date == 'null':
        opening_date_check = True
    elif stabilization_date > opening_date:
            opening_date_check = True
    return opening_date_check

def CheckStabilizationDate(submittal_id):
    submittal = Submittal.objects.get(id=submittal_id)
    property_id = submittal.prop_id
    property = Property.objects.get(id=property_id)
    stabilization_date = property.date_stabilization
    leasing_status = submittal.leasing_status
    stabilization_date_complete = 'incomplete'
    if leasing_status == 'stabilized':
        minimum_date = datetime.date(year=2010, month=1, day=1)
        if stabilization_date <> None:
            if stabilization_date >= minimum_date:
                stabilization_date_complete = 'complete'
    elif leasing_status == 'leaseup':
        stabilization_date_complete = 'complete'
    return stabilization_date_complete


def PriorMonthSubmittalDates(submittal_id):
    submittal = Submittal.objects.get(id=submittal_id)
    current_year = submittal.submittal_year
    current_month = submittal.submittal_month
    prior_year = None
    prior_month = None
    if current_month == 1:
        prior_year = current_year - 1
        prior_month = 12
    else:
        prior_year = current_year
        prior_month = current_month - 1
    prior_period = {
        'prior_year': prior_year,
        'prior_month': prior_month,
    }
    return prior_period

def DateYearChoices():
    year_choices = []
    for i in range(2010, 2100, 1):
        year_choices.append((i, i),)
    return year_choices

def DateMonthChoices():
    month_choices = []
    for i in range(1, 13, 1):
        month_choices.append((i, i),)
    return month_choices

def DateDayChoices():
    day_choices = []
    for i in range(1, 32, 1):
        day_choices.append((i, i),)
    return  day_choices

def DateChoices():
    year_choices = DateYearChoices()
    month_choices = DateMonthChoices()
    day_choices = DateDayChoices()
    choices = {
        'year_choices': year_choices,
        'month_choices': month_choices,
        'day_choices': day_choices,
    }
    return choices

def CheckDates(year, month, day):
    dates_okay = True
    leap_year = False
    delta_year = 0
    if year > 2008:
        delta_year = int(year) - 2008
        if (delta_year % 4 == 0):
            leap_year = True
    if month == 2:
        if leap_year == False:
            if day > 28:
                dates_okay = False
        else:
            if day > 29:
                dates_okay = False
    if (month == 4) or (month == 6) or (month == 9) or (month == 11):
        if day > 30:
            dates_okay = False
    current_date = datetime.date.today()
    entered_date = datetime.date(year=int(year), month=int(month), day=int(day))
    if entered_date > current_date:
        dates_okay = False
    return dates_okay