# Generated by Django 4.2.2 on 2023-06-29 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpine_fees', '0002_alter_feereceipts_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feereceipts',
            name='enrol_id',
            field=models.CharField(max_length=100),
        ),
    ]
