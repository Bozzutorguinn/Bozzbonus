from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from property.models import Property

def CheckAuthorization(request, property_id):
    property = Property.objects.get(id=property_id)
    user = request.user
    rm_user = property.rm_user
    authorized_user = False
    if user.id == rm_user.id:
        authorized_user = True
        return authorized_user
    else:
        return HttpResponseRedirect(reverse('property:index'))