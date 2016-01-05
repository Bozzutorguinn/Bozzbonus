from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Property
from submittal.models import Submittal

@login_required
def PropertyIndex(request):
    user_id = request.user
    properties = Property.objects.filter(rm_user_id=user_id)
    context = {'properties': properties}
    return render(request, 'property/index.html', context)

@login_required
def PropertyDetail(request, property_id):
    user_id = request.user
    property = Property.objects.get(id=property_id)
    user = property.rm_user
    if user.id == user_id.id:
        open_submittals = Submittal.objects.filter(prop=property_id, pm_submitted=0)
        context = {'open_submittals': open_submittals, 'property': property}
        return render(request, 'property/property_submittals.html', context)
    else:
        #re-direct the user to a listing of the properties that they do have access to
        return PropertyIndex(request)