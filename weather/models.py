from django.db import models

# Create your models here.
from weather.managers import CityWeatherManager


class City(models.Model):

    name = models.CharField(max_length=256)
    state = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    latitude = models.CharField(max_length=64)
    longitude = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class CityWeather(models.Model):

    FREQUENCY_CHOICES = [
        ('DAILY', 'DAILY'),
        ('MINUTELY', 'MINUTELY'),
        ('HOURLY', 'HOURLY'),
    ]

    city = models.ForeignKey('City', on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    frequency = models.CharField(max_length=8, choices=FREQUENCY_CHOICES, default="DAILY")
    weather = models.CharField(max_length=256)
    sunrise = models.DateTimeField()
    sunset = models.DateTimeField()
    moonrise = models.DateTimeField()
    moonset = models.DateTimeField()
    pressure = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    wind_deg = models.FloatField()
    wind_gust = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    temp_day = models.FloatField()
    temp_night = models.FloatField()
    temp_evening = models.FloatField()
    temp_morning = models.FloatField()


    objects = CityWeatherManager()

    def __str__(self):
        return self.city.name + " - " +  str(self.date)

