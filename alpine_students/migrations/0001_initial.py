# Generated by Django 4.2.2 on 2023-06-23 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('college_id', models.IntegerField()),
                ('crsid', models.IntegerField()),
                ('ssnid', models.IntegerField()),
                ('enrol_id', models.CharField(max_length=100, unique=True)),
                ('stu_name', models.CharField(max_length=200)),
                ('doj', models.CharField(max_length=200)),
                ('contact_no', models.CharField(blank=True, max_length=200, null=True)),
                ('admsn_fee', models.IntegerField(blank=True, null=True)),
                ('security_fee', models.IntegerField(blank=True, null=True)),
                ('other_fee', models.IntegerField(blank=True, null=True)),
                ('yr1_fee', models.IntegerField(blank=True, null=True)),
                ('yr2_fee', models.IntegerField(blank=True, null=True)),
                ('yr3_fee', models.IntegerField(blank=True, null=True)),
                ('yr4_fee', models.IntegerField(blank=True, null=True)),
                ('yr5_fee', models.IntegerField(blank=True, null=True)),
                ('yr6_fee', models.IntegerField(blank=True, null=True)),
                ('ref_by', models.IntegerField(blank=True, null=True)),
                ('is_paid', models.CharField(blank=True, max_length=20, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
