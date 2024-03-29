# Generated by Django 4.2.1 on 2024-02-14 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=200, unique=True)),
                ('overview', models.TextField()),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ['department_name'],
            },
        ),
        migrations.CreateModel(
            name='PersonalDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=1)),
                ('address', models.TextField()),
                ('zipcode', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('picture', models.ImageField(null=True, upload_to='patients')),
                ('is_doctor', models.BooleanField(default=False, null=True)),
                ('is_reception', models.BooleanField(default=False, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(null=True)),
                ('personal_details', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.personaldetail')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['personal_details'],
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField()),
                ('education', models.CharField()),
                ('speciality', models.CharField()),
                ('picture', models.ImageField(upload_to='doctors')),
                ('doctor_Number', models.CharField(default=False, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.department')),
                ('personal_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.personaldetail')),
            ],
            options={
                'ordering': ['personal_details'],
            },
        ),
        migrations.CreateModel(
            name='booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('date_booked', models.DateField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('attended', models.BooleanField(default=False, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.department')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.doctor')),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.patient')),
            ],
            options={
                'ordering': ['date_booked'],
            },
        ),
    ]
