from django.db import models
from django.utils.timezone import now

# Create your models here.


class User_Manager(models.Manager):
    def create_User(self, _username, _password, _email, _name):
        book = self.create(username=_username,
                           password=_password, email=_email, name=_name)
        book.save()
        return book


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=20)
    chp_staff_number = models.CharField(max_length=7)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    objects = User_Manager()


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=200)
    date_of_birth = models.DateField(editable=True)

    def __str__(self):
        return self.name


class InfectingVirus(models.Model):
    virus_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    common_name = models.CharField(max_length=200)
    max_infectious_period = models.IntegerField(
        default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.common_name})'


class Coordinate(models.Model):
    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'({self.x}, {self.y})'


class Location(models.Model):
    category_choice = [('R', 'Residence'), ('W', 'Workplace'), ('V', 'Visit')]

    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date_from = models.DateTimeField(default=now, editable=True)
    date_to = models.DateTimeField(default=now, editable=True)
    category = models.CharField(
        max_length=30, choices=category_choice, default='R')

    grid_coordinates = models.ForeignKey(Coordinate, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.location_id}: {self.location_name} ({self.category})'


class ConfirmedCase(models.Model):
    local_or_imported = [('Local', 'Local'), ('Imported', 'Imported')]

    case_id = models.AutoField(primary_key=True)
    case_number = models.CharField(max_length=10)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    virus_id = models.ForeignKey(InfectingVirus, on_delete=models.CASCADE)
    date = models.DateField(default=now, editable=True)
    category = models.CharField(
        max_length=20, choices=local_or_imported, default='Local')
    
    location = models.ManyToManyField(Location)

    def __str__(self):
        return f'{self.case_number}: {self.patient_id}, {self.category} ({self.virus_id})'
