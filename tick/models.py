from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from mysite.constants.others import PAYMENT_METHODS, PAYMENT_PROVIDER, TRANSACTION_STATUSES

# Create your models here.

YES_OR_NO = (
    # ('__', '__'),
    ('Yes', 'Yes'),
    ('No', 'No'),
)

GENDER = (
    # ('__', '__'),
    ('Male', 'Male'),
    ('Female', 'Female'),
)

HOSTEL_CLASS = (
    ('National', 'National'),
    ('Diocease', 'Diocease'),
    ('Regular', 'Regular'),
)

LOCATION_TYPE = (
    ('Online', 'Online'),
    ('Physical', 'Physical'),
)

TICKET_TYPE = (
    ('Free', 'Free'),
    ('Paid', 'Paid'),
    ('Donation', 'Donation'),
)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    title = models.CharField(null=False, blank=False, max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200, default="Online", choices=LOCATION_TYPE)
    venue = models.CharField(null=True, blank=True, max_length=200)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    banner = models.ImageField(null=True, blank=True)
    ticket_available = models.IntegerField(default=0)
    ticket_type = models.CharField(default='Free', max_length=50, choices=TICKET_TYPE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Tick(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, null=True, blank=True)
    ref = models.CharField(null=False, blank=False, max_length=10)
    email = models.EmailField(max_length=254, null=False, blank=False, unique=True)
    first_name = models.CharField(null=False, blank=False, max_length=100)
    last_name = models.CharField(null=False, blank=False, max_length=100)
    middle_name = models.CharField(null=True, blank=True, max_length=100)
    gender = models.CharField(null=False, blank=False, max_length=10, choices=GENDER)
    phone = models.CharField(null=False, blank=False, unique=True, max_length=15)
    institution = models.CharField(null=True, blank=True, max_length=300)
    diocese = models.CharField(null=True, blank=True, max_length=100)
    parish = models.CharField(null=True, blank=True, max_length=100)
    are_you_a_Watchman = models.CharField(null=False, blank=False, max_length=10, choices=YES_OR_NO)
    created_at = models.DateTimeField(default=timezone.now)
    img = models.ImageField(null=True, blank=True, upload_to='preview')
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f'{ self.first_name } {self.last_name}'


class Hostel(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    gender_type = models.CharField(null=False, blank=False, max_length=10, choices=GENDER)
    hostel_class = models.CharField(null=False, blank=False, max_length=10, choices=HOSTEL_CLASS)
    rooms_available = models.IntegerField(blank=True, null=True)
    booked = models.ManyToManyField(Tick, blank=True, related_name='booked')
    lodgers = models.ManyToManyField(Tick, blank=True, related_name='tickets')

    picture_1 = models.ImageField(blank=True, null=True, upload_to='hostel_pics')
    picture_2 = models.ImageField(blank=True, null=True, upload_to='hostel_pics')
    picture_3 = models.ImageField(blank=True, null=True, upload_to='hostel_pics')
    picture_4 = models.ImageField(blank=True, null=True, upload_to='hostel_pics')

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{ self.name } Hostel'


class Transaction(models.Model):
    transaction_ref = models.CharField(max_length=100, null=False, blank=False)
    ticket = models.ForeignKey(Tick, null=False, blank=False, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHODS, null=False, blank=False
    )
    payment_provider = models.CharField(
        max_length=50, choices=PAYMENT_PROVIDER, null=False, blank=False
    )
    discount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    vat = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    total_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    verified = models.BooleanField(default=False)
    transaction_status = models.CharField(
        max_length=200,
        choices=TRANSACTION_STATUSES,
        null=True,
        blank=True,
        default="Pending Payment",
    )
    transaction_description = models.CharField(max_length=200, null=True, blank=True)
