from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Property

@login_required
def PropertyIndex(request):
    user_id = request.user
    properties = Property.objects.filter(rm_user_id=user_id)
    context = {'properties': properties}
    return render(request, 'property/index.html', context)