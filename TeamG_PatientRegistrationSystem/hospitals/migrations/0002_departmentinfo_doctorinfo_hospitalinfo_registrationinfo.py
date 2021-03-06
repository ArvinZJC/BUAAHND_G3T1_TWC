# Generated by Django 2.1.2 on 2018-11-09 12:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospitals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('brief_introduction', models.CharField(max_length=200, verbose_name='brief introduction')),
                ('detail', models.TextField(unique=True, verbose_name='more details')),
                ('director', models.CharField(max_length=60, unique=True, verbose_name='director')),
                ('tel', models.CharField(max_length=20, unique=True, verbose_name='tel.')),
            ],
            options={
                'verbose_name': 'Department',
            },
        ),
        migrations.CreateModel(
            name='DoctorInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brief_introduction', models.CharField(max_length=100, verbose_name='brief introduction')),
                ('detail', models.TextField(unique=True, verbose_name='more details')),
                ('is_available', models.BooleanField(default=True, verbose_name='available')),
                ('is_expert', models.BooleanField(default=False, verbose_name='expert')),
            ],
            options={
                'verbose_name': 'Doctor',
            },
        ),
        migrations.CreateModel(
            name='HospitalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='name')),
                ('brief_introduction', models.CharField(max_length=300, verbose_name='brief introduction')),
                ('detail', models.TextField(unique=True, verbose_name='more details')),
                ('address', models.CharField(max_length=100, unique=True, verbose_name='address')),
                ('director', models.CharField(max_length=60, unique=True, verbose_name='director')),
                ('tel', models.CharField(max_length=20, unique=True, verbose_name='tel.')),
            ],
            options={
                'verbose_name': 'Hospital',
            },
        ),
        migrations.CreateModel(
            name='RegistrationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_time', models.DateTimeField(verbose_name='appointment time')),
                ('submission_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='submission time')),
                ('status', models.CharField(choices=[('1', 'Awaiting confirmation'), ('2', 'Accepted'), ('3', 'Failed'), ('4', 'Completed')], default='1', max_length=30, verbose_name='status')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.DoctorInfo', verbose_name='doctor')),
            ],
            options={
                'verbose_name': 'Registration',
                'verbose_name_plural': 'Registration',
            },
        ),
    ]
