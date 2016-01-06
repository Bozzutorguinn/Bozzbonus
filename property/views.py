from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Property
from submittal.models import Submittal
from user_access.tools import CheckAuthorization

@login_required
def PropertyIndex(request):
    user_id = request.user
    properties = Property.objects.filter(rm_user_id=user_id)
    context = {'properties': properties}
    return render(request, 'property/index.html', context)

@login_required
def PropertyDetail(request, property_id):
    property = Property.objects.get(id=property_id)
    authorized_user = CheckAuthorization(request, property_id)
    if authorized_user == True:
        open_submittals = Submittal.objects.filter(prop=property_id, pm_submitted=0)
        submitted_submittals = Submittal.objects.filter(prop=property_id, pm_submitted=1)
        context = {'open_submittals': open_submittals,
                   'submitted_submittals': submitted_submittals,
                   'property': property,
                   }
        return render(request, 'property/property_submittals.html', context)