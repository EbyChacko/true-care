# Generated by Django 4.2.1 on 2024-02-01 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_patient_password_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patient_age',
            field=models.CharField(),
        ),
    ]