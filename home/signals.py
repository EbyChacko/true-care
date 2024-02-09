from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Patient, PersonalDetail

@receiver(post_save, sender=User)
def create_patient(sender,instance, created, **kwargs):
    if not PersonalDetail.objects.filter(email=instance.email).exists():
        personal_details = PersonalDetail.objects.create(name=instance.username, email=instance.email)
        Patient.objects.create(user=instance, personal_details=personal_details, date_of_birth=None)
        print('user created')
post_save.connect(create_patient,sender=User)


@receiver(post_save, sender=User)
def update_patient(sender,instance, created, **kwargs):
    if created==False:
        instance.patient.save()
    