from __future__ import unicode_literals
from property.models import Property
from django.db import models

class Submittal(models.Model):
    prop = models.ForeignKey(Property)
    submittal_year = models.IntegerField(default=0)
    submittal_month = models.IntegerField(default=0)
    #boolean 0/1 field; 0 is not submitted and 1 is submitted
    #indicates whether or not the property manager has completed the form and submitted the bonus
    pm_submitted = models.IntegerField(default=0)
    #boolean 0/1 field; 0 is not approved yet and 1 is approved
    #indicates whether the RM has approved the bonus after having reviewed it
    rm_approved = models.IntegerField(default=0)
    #boolean 0/1 field; 0 is not approved yet and 1 is approved
    #indicates whether the bonus has been submitted to payroll for processing after RM approval
    #in typical usage, should automatically be marked as submitted once the scheduled submittal process runs
    payroll_submitted = models.IntegerField(default=0)
    occupancy_rate = models.DecimalField(max_digits=4,decimal_places=1, null=True)
    #options are leaseup and stabilized
    #pre_leasing for the application bonus will be determined based on applications submitted prior to the date
    #of the first move-in
    leasing_status = models.CharField(max_length=20, null=True)
    op_rev_month_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    op_rev_month_actual = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    noi_semi_ann_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    noi_semi_ann_actual = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    op_rev_qtr_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    op_rev_qtr_actual = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    #boolean 0/1 field; 0 is no override bonus and 1 is that that bonus is approved
    lease_up_override = models.IntegerField(default=0)
    delinquency_rate = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    #boolean 0/1 field; 0 is that there were no bad debt write-offs and 1 is that there were
    bad_debt_writeoffs = models.IntegerField(default=0)
    #this is a check to confirm whether all necessary information for the submittal has been entered
    #before allowing the user to calculate specific bonus amounts
    #0/1 boolean with 0 not submitted and 1 is fully submitted
    #will be used as a toggle in the view to allow specific bonus amounts to be calculated
    data_complete = models.IntegerField(default=0)