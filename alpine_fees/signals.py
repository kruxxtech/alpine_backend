from django.db.models.signals import post_save
from django.dispatch import receiver
from alpine_fees.models import FeeReceipts, FeeBalance


#  Signal to update feebalance after fee receipt is created
@receiver(post_save, sender=FeeReceipts)
def update_fee_balance(sender, instance, created, **kwargs):
    print("reached jerer", instance.year)
    if created:
        print("reached jerer", instance.year)
        # Fetch the FeeBalance instance for the student
        fee_balance = FeeBalance.objects.get(
            student_id=instance.student_id, curr_year=instance.year
        )

        # Update the FeeBalance instance
        fee_balance.reg_fee = fee_balance.reg_fee - instance.reg_fee
        fee_balance.sec_fee = fee_balance.sec_fee - instance.sec_fee
        fee_balance.tut_fee = fee_balance.tut_fee - instance.tut_fee
        fee_balance.other_fee = fee_balance.other_fee - instance.other_fee
        fee_balance.rebate = fee_balance.rebate - instance.rebate
        fee_balance.pre_bal = fee_balance.pre_bal - instance.pre_bal

        # Save the updated FeeBalance instance
        fee_balance.save()
