# Generated by Django 4.2.1 on 2024-02-19 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_reportnames_medicalreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalreport',
            name='report_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.reportnames'),
        ),
    ]