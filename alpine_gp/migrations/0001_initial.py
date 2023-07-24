# Generated by Django 4.2.2 on 2023-07-24 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('agentsid', models.BigIntegerField(primary_key=True, serialize=False)),
                ('agentname', models.CharField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('contact', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('college_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('college_code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('website', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=200)),
                ('affiliation', models.CharField(max_length=200, null=True)),
                ('approved_by', models.CharField(max_length=200, null=True)),
                ('status', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('ssnid', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('ssntitle', models.TextField()),
                ('sdate', models.CharField()),
                ('edate', models.CharField()),
                ('iscurrent', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('crsid', models.BigIntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('course', models.CharField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('college', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='alpine_gp.college')),
            ],
        ),
    ]
