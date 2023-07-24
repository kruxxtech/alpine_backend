from django.db.models.signals import post_save
from django.dispatch import receiver
from alpine_students.models import Admission, Promotion

from alpine_fees.models import FeeBalance


@receiver(post_save, sender=Admission)
def create_fee_balance(sender, instance, created, **kwargs):
    if created:
        FeeBalance.objects.create(
            student=instance,
            reg_fee=instance.admsn_yr1,
            sec_fee=instance.security_fee,
            tut_fee=instance.yr1_fee,
            other_fee=instance.other_fee,
            pre_bal=0,
            rebate=0,
            curr_year=1,
        )


@receiver(post_save, sender=Promotion)
def update_fee_balance(sender, instance, **kwargs):
    print(instance.status)
    if instance.status == "promoted":
        print("reached jerer", instance.curr_year)

        fee_balance_old = FeeBalance.objects.get(
            student_id=instance.student_id, curr_year=instance.curr_year - 1
        )
        print(fee_balance_old)
        new_pre_bal = (
            fee_balance_old.pre_bal
            + fee_balance_old.reg_fee
            + fee_balance_old.sec_fee
            + fee_balance_old.tut_fee
            + fee_balance_old.other_fee
            - fee_balance_old.rebate
        )

        # Fetch the Admission instance for the student
        admission = Admission.objects.get(student_id=instance.student_id)

        tution_fee = "yr" + str(instance.curr_year) + "_fee"
        # create new fee balance
        FeeBalance.objects.create(
            student_id=instance.student_id,
            reg_fee=0,
            sec_fee=admission.security_fee,
            tut_fee=admission.__getattribute__(tution_fee),
            other_fee=admission.other_fee,
            pre_bal=new_pre_bal,
            rebate=0,
            curr_year=instance.curr_year,
        )
