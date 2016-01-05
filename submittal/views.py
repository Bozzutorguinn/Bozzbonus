from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from property.models import Property
from .models import Submittal

@login_required
def SubmittalDetail(request, submittal_id):
    user_id = request.user
    submittal = Submittal.objects.get(id=submittal_id)
    property_id = submittal.prop_id
    property = Property.objects.get(id=property_id)
    rm_user = property.rm_user
    #check that the logged-in user is authorized to view the property
    if user_id.id == rm_user.id:
        #convert the boolean 0/1 for lease-up override to 'yes' or 'no'
        lease_up_override = 'No'
        if submittal.lease_up_override == 1:
            lease_up_override = 'Yes'
        #convert the boolean 0/1 for bad debt writeoff to 'yes' or 'no'
        bad_debt_writeoff = 'No'
        if submittal.bad_debt_writeoffs == 1:
            bad_debt_writeoff = 'Yes'
        context = {'submittal': submittal,
                   'property': property,
                   'lease_up_override': lease_up_override,
                   'bad_debt_writeoff': bad_debt_writeoff,
                   }
        return render(request, 'submittal/submittal_detail.html', context)
    else:
        #re-direct the user to a listing of the properties that they do have access to
        return HttpResponseRedirect(reverse('property:index'))