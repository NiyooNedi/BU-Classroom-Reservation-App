# File: models.py
# Author: Niyoo Nedi (nnedi@bu.edu), 4/20/2026
# Description: File that will contain the models for my final project

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta
    
    
class Building(models.Model):
    '''encapsulate the building data'''

    abr_name = models.CharField(max_length=3)
    address = models.CharField(max_length=50)
    side_of_campus = models.CharField(max_length=50)
    num_rooms = models.IntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        '''str rep of a building'''
        return f"{self.abr_name} - {self.address}"
    


class Microphone(models.Model):
    '''encapsulate the microphone data'''

    mic_types = [("lav", "Lavalier"), ("handheld", "Handheld"), ("shotgun", "Shotgun")]

    type = models.CharField(max_length=20, choices=mic_types)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    wireless = models.BooleanField()
    name = models.CharField(max_length=100)

    def __str__(self):
        '''str rep of a microphone'''
        return f"{self.name}"



class Room(models.Model):
    '''encapsulate the room data'''

    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    room_num = models.IntegerField()
    projector = models.BooleanField()
    mic_count = models.IntegerField()
    microphones = models.ManyToManyField(Microphone, blank=True)

    def __str__(self):
        '''str rep of a building's room '''
        return f"{self.building.abr_name} {self.room_num}"
    


class Booking(models.Model):
    '''encapsulate the booking data'''

    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def checks(self):
        '''method to check if the current booking should be allowed or not'''

        #making sure the start must be before end
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

        #var for building and its times
        building = self.room.building
        opening_time = building.opening_time
        closing_time = building.closing_time

        #check if the reservation is within the building hours
        if self.end_time.time() > closing_time:
            raise ValidationError("Booking extends past building closing time.")
        if self.start_time.time() < opening_time:
            raise ValidationError("Booking starts before building opening time.")
        #checks that the reservation is not more than 3 hours
        if self.end_time - self.start_time > timedelta(hours=3):
            raise ValidationError("Bookings cannot be longer than 3 hours.")

        #check if this current booking overlaps with another booking
        overlapping = Booking.objects.filter(room = self.room, start_time__lt = self.end_time, end_time__gt = self.start_time,)
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        #raise an error if it overlaps
        if overlapping.exists():
            raise ValidationError("This room is already booked for that time.")

    def save(self, *args, **kwargs):
        '''func that runs before the booking gets saved, which will call the check func'''
        self.checks()
        super().save(*args, **kwargs)

    def __str__(self):
        '''str rep of a user's booking'''
        return f"{self.user} booked {self.room}"
