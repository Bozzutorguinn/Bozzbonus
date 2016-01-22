from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from property.models import Property
from .models import Submittal_Employees
from employees.models import Employees
from submittal.models import Submittal
#from .forms import
from user_access.tools import CheckAuthorization
from .tools import SubmittalEmployees


@login_required
def EditEmployees(request, submittal_id):
    submittal_employees = SubmittalEmployees(submittal_id=submittal_id)
    submittal = Submittal.objects.get(id=submittal_id)
    property_id = submittal.prop_id
    property = Property.objects.get(id=property_id)
    #check that the logged-in user is authorized to view the property
    authorized_user = CheckAuthorization(request, property_id)
    if authorized_user == True:
        context = {'submittal': submittal,
                   'submittal_employees': submittal_employees,
                   'property': property,
                   }
        return render(request, 'submittal/submittal_detail.html', context)

@login_required
def RemoveEmployee(request, submittal_id, employee_id):
    pass