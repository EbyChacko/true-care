from django.db import migrations, models

def set_default_values(apps, schema_editor):
    Doctor = apps.get_model('home', 'Doctor')
    for doctor in Doctor.objects.all():
        doctor.doctor_Number = ''  # Set default value for is_doctor field
        doctor.save()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),  
    ]

    operations = [
        
        migrations.AddField(
            model_name='doctor',
            name='doctor_Number',
            field=models.CharField(null=True),
        ),
        migrations.RunPython(set_default_values),
    ]
