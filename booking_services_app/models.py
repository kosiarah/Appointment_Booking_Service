from django.db import models

# class consumer
# class service_provider
# class admin?
# class appointment


class User(models.Model):
    USER_TYPE_CHOICES = (
        ('service_provider', 'Service Provider'),
        ('consumer', 'Consumer')
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    user_name = models.CharField(max_length=120)
    user_age = models.IntegerField(default=0)
    user_email = models.EmailField()
    user_phone_number = models.CharField(max_length=120)
    user_password = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class Appointment(models.Model):
    appointment_name = models.CharField(max_length=120)
    appointment_date = models.DateField()
    appointment_description = models.TextField()
    appointment_price = models.DecimalField(max_digits=5, decimal_places=2)
    appointment_location = models.TextField()
    appointment_duration = models.TextField()
    appointment_service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', limit_choices_to={'user_type': 'service_provider'})
    appointment_consumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_appointment', limit_choices_to={'user_type': 'consumer'})