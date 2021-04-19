from django.db import models
from django.db.models.functions import Coalesce

from weather.utils import get_weather_forecast_data


class CityWeatherManager(models.Manager):

    def get_weather_details(self, cities, date):
        for city in cities:
            print(city.name)
            weather_details = self.filter(city=city, date=date)
            if not weather_details:
                get_weather_forecast_data(city)

        weather_details = self.filter(city__in=cities, date=date)
        return weather_details

    def get_weather_by_type(self, cities, date, weather):
        for city in cities:
            weather_details = self.filter(city=city, date=date)
            if not weather_details:
                get_weather_forecast_data(city)

        weather_details = self.filter(city__in=cities, date=date, weather__in=weather)
        return weather_details

    def get_hottest_cities(self, cities, date):
        for city in cities:
            weather_details = self.filter(city=city, date=date)
            if not weather_details:
                get_weather_forecast_data(city)

        weather_details = self.filter(city__in=cities, date=date).order_by("-temp_max")[:3]
        return weather_details
