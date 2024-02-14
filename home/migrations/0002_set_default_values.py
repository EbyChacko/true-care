from django.db import migrations, models

def set_default_values(apps, schema_editor):
    PersonalDetail = apps.get_model('home', 'PersonalDetail')
    for personal_detail in PersonalDetail.objects.all():
        personal_detail.is_doctor = False  # Set default value for is_doctor field
        personal_detail.is_reception = False  # Set default value for is_reception field
        personal_detail.save()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),  
    ]

    operations = [
        migrations.AddField(
            model_name='personaldetail',
            name='is_doctor',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='personaldetail',
            name='is_reception',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.RunPython(set_default_values),
    ]
