def SubmittalEmployees(submittal_id):
    submittal_employees = Submittal_Employees.objects.filter(submittal_id=submittal_id)
    employees = []
    for submittal_employee in submittal_employees:
        employee = Employees.objects.get(id=submittal_employee.employee_id)
        employees.append(employee)
    return employees
