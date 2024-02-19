from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

# department model
class Department(models.Model):
    department_name = models.CharField(max_length=200, unique=True)
    overview = models.TextField()
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['department_name']

    def __str__(self):
        return self.department_name

# model for the personal details
class PersonalDetail(models.Model):
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length=1, default='M', choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    address = models.TextField()
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    picture = models.ImageField(upload_to='patients', null=True, )
    is_doctor = models.BooleanField(default=False, null=True)
    is_reception = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# model for the details of doctors
class Doctor(models.Model):
    personal_details = models.OneToOneField(PersonalDetail, on_delete=models.CASCADE)
    designation = models.CharField()
    education = models.CharField()
    speciality = models.CharField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='doctors')
    doctor_Number =  models.CharField(default=False, null=True)
    
    class Meta:
        ordering = ['personal_details']

    def __str__(self):
         return f"{self.personal_details}"

@receiver(post_save, sender=PersonalDetail)
def create_or_update_doctor(sender, instance, created, **kwargs):
    if created or instance.is_doctor:
        department = Department.objects.first()
        doctor, _ = Doctor.objects.get_or_create(personal_details=instance, defaults={'department': department})
        
        # Check if the doctor instance already exists and update fields only if they are empty
        if not doctor.designation:
            doctor.designation = ''
        if not doctor.education:
            doctor.education = ''
        if not doctor.speciality:
            doctor.speciality = ''
        if not doctor.picture:
            doctor.picture = ''
        if not doctor.doctor_Number:
            doctor.doctor_Number = ''
        
        doctor.save()


#model for the patients details
class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    personal_details = models.OneToOneField(PersonalDetail, null=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)

    class Meta:
        ordering = ['personal_details']

    def __str__(self):
         return f"{self.personal_details}"
    


# model for the booing details
class booking(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    booking_date = models.DateField()
    date_booked = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    attended = models.BooleanField(default=False, null=True)
    class Meta:
        ordering = ['date_booked']

    def __str__(self):
         return f"{self.id}: Booking by {self.patient_id} at {self.department} department for {self.doctor}"


# model fo the customer message from the contact.html
class CustomerMessage(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

# model for the doctor diagnosis details
class DoctorDiagnosis(models.Model):
    booking = models.ForeignKey(booking, on_delete=models.CASCADE)
    height = models.CharField()
    weight =models.CharField()
    bp = models.CharField()
    pulse = models.CharField()
    saturation = models.CharField()
    temperature = models.CharField()
    allergy = models.TextField()
    medical_history = models.TextField()
    medications = models.TextField()
    present_complaints = models.TextField()
    physical_examination = models.TextField(null=True)
    diagnosis = models.TextField()

    def __str__(self):
        return f"{self.booking.patient_id}'s Diagnosis by {self.booking.doctor} on {self.booking.booking_date}"


# model for prescription
class Prescription(models.Model):
    booking = models.ForeignKey(booking, on_delete=models.CASCADE)
    drug_name = models.CharField()
    dose = models.CharField()
    frequency = models.CharField()
    route = models.CharField()
    quantity = models.CharField()
    comment = models.TextField(null=True)
    def __str__(self):
        return f"{self.booking}, {self.drug_name}"

# model for Report names
class ReportNames(models.Model):
    report_name = models.CharField()
    def __str__(self):
        return self.report_name

# model for medical reports
class MedicalReport(models.Model):
    booking = models.ForeignKey(booking, on_delete=models.CASCADE)
    report_name = models.ForeignKey(ReportNames, on_delete=models.CASCADE)
    report = models.FileField(upload_to='medical_reports', blank=True)
    def __str__(self):
        return f"{self.booking}, {self.report_name}"