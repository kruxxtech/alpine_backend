from django.db import models
from alpine_students.models import Admission, Profile
from alpine_gp.models import Course, College, Session


# Create your models here.
class FeeTable(models.Model):
    fee_id = models.AutoField(primary_key=True, editable=False, null=False)
    college_id = models.BigIntegerField()
    ssnid = models.BigIntegerField()
    crsid = models.CharField()

    security = models.BigIntegerField()
    other = models.BigIntegerField()

    admsn_yr1 = models.BigIntegerField(null=True)
    admsn_yr2 = models.BigIntegerField(null=True)
    admsn_yr3 = models.BigIntegerField(null=True)
    admsn_yr4 = models.BigIntegerField(null=True)
    admsn_yr5 = models.BigIntegerField(null=True)
    admsn_yr6 = models.BigIntegerField(null=True)

    yr1 = models.BigIntegerField(null=True)
    yr2 = models.BigIntegerField(null=True)
    yr3 = models.BigIntegerField(null=True)
    yr4 = models.BigIntegerField(null=True)
    yr5 = models.BigIntegerField(null=True)
    yr6 = models.BigIntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def total_fee(self):
        return (
            self.admsn_yr1
            + self.security
            + self.other
            + self.yr1
            + self.yr2
            + self.yr3
            + self.yr4
            + self.yr5
            + self.yr6
        )


class FeeReceipts(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    student = models.ForeignKey(Admission, on_delete=models.CASCADE)
    enrol_id = models.CharField(max_length=100)
    stu_name = models.CharField(max_length=100)
    reg_fee = models.DecimalField(max_digits=8, decimal_places=2)
    sec_fee = models.DecimalField(max_digits=8, decimal_places=2)
    tut_fee = models.DecimalField(max_digits=8, decimal_places=2)
    other_fee = models.DecimalField(max_digits=8, decimal_places=2)
    pre_bal = models.DecimalField(max_digits=8, decimal_places=2)
    rebate = models.DecimalField(max_digits=8, decimal_places=2)
    year = models.IntegerField()
    fee_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Receipt #{self.pk} - Student: {self.stu_name}"


class FeeBalance(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    student = models.ForeignKey(Admission, on_delete=models.CASCADE)
    reg_fee = models.DecimalField(max_digits=8, decimal_places=2)
    sec_fee = models.DecimalField(max_digits=8, decimal_places=2)
    tut_fee = models.DecimalField(max_digits=8, decimal_places=2)
    other_fee = models.DecimalField(max_digits=8, decimal_places=2)
    pre_bal = models.DecimalField(max_digits=8, decimal_places=2)
    rebate = models.DecimalField(max_digits=8, decimal_places=2)
    curr_year = models.IntegerField()

    def __str__(self):
        return f"Balance #{self.pk}"
