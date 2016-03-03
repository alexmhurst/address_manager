from django.db import models
from django.utils import timezone
from addman.google_usps_validator import GoogleUspsValidator


# Create your models here.

class AddressSet(models.Model):
    set_name = models.CharField(max_length=150)
    set_description = models.CharField(max_length=1000, blank=True)
    creation_time = models.DateTimeField('date created', default=timezone.now)
    update_time = models.DateTimeField('date updated', default=timezone.now)
    owner = models.CharField(max_length=30)

    def __str__(self):
        return self.set_name


class Address(models.Model):

    UNPARSED = 'UNPARSED'
    FAILED = 'FAILED'
    WARN = 'WARN'
    CONFIRMABLE = 'CONFIRMABLE'
    VALIDATED = 'VALIDATED'

    STATUS_CHOICES = (
        (UNPARSED, 'Not yet processed'),
        (FAILED, 'No match found'),
        (WARN, 'Tentative match, may be undeliverable'),
        (CONFIRMABLE, 'Tentative match, confirmation required'),
        (VALIDATED, 'Validated and deliverable'),
    )

    creation_time = models.DateTimeField('date created', default=timezone.now)
    address_set = models.ForeignKey(AddressSet)
    user_input = models.CharField(max_length=1000)

    street = models.CharField(blank=True, max_length=1000)
    city = models.CharField(blank=True, max_length=1000)
    state = models.CharField(blank=True, max_length=2)
    zip = models.CharField(blank=True, max_length=5)

    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES,
                              default=UNPARSED)

    message = models.TextField(blank=True)

    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.user_input

    def validate(self):
        validator = GoogleUspsValidator()
        result = validator.validate(self.user_input)

        self.city = result['status']
        self.message = result['message']
        if self.city in ['CONDITIONAL', 'MAPPED']:
            self.street = result['address']['formatted_address']
        else:
            self.street = 'not found yet'
        self.save()


        # self.street = processed_address.data['street']
        # self.city = processed_address.data['city']
        # self.state = processed_address.data['state']
        # self.zip = processed_address.data['zip']
        #
        # self.validation_message = processed_address.message
        # self.status = processed_address.status
