# Generated by Django 4.2.2 on 2023-06-29 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alpine_gp', '0001_initial'),
        ('alpine_students', '0009_alter_promotion_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='duration',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='alpine_gp.course'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='promotion',
            name='status',
            field=models.CharField(choices=[('promoted', 'Promoted'), ('not_promoted', 'Not Promoted'), ('passed', 'Passed'), ('suspended', 'Suspended')], default='not_passed', max_length=20),
        ),
    ]
