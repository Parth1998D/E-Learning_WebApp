from django.core.exceptions import ValidationError
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=False, null=False, default='')

    def __str__(self):
        return self.name


# Q-9
def validate_price(value):
    if value < 50 or value > 500:
        raise ValidationError('Course Price should be between $50 and $500')


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    # [MinValueValidator(50), MaxValueValidator(500)])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.name

    def discount(self):
        return 90 * self.price / 100


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgary'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Order(models.Model):
    STATUS = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, related_name='orders', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='orders', on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=STATUS, default=1)
    order_date = models.DateTimeField()

    def __str__(self):
        return str(self.order_status) + " " + self.student.first_name

    def total_cost(self):
        return self.course.price


class PasswordReset(models.Model):
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.username
