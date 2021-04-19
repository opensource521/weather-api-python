import requests
import datetime
from weather import models


def get_weather_forecast_data(city):
    """
    Author: Hardik Chauhan
    :param city:
    :return: Forecast data for given city
    """
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&exclude=minutely,hourly&appid=9ccebc1f5720273f5f2e0ca6ec867c83"
    response = requests.get(url.format(lat=city.latitude, long=city.longitude))
    if response.status_code == 200:
        json_data = response.json()
        city_weather_values = []
        for day_wise in json_data['daily']:
            # TODO: need to write logic to avoid duplicate entries
            city_weather_values.append(
                models.CityWeather(
                    city=city,
                    date=datetime.datetime.fromtimestamp(day_wise['dt']).date(),
                    frequency="DAILY",
                    sunrise=datetime.datetime.fromtimestamp(day_wise['sunrise']),
                    sunset=datetime.datetime.fromtimestamp(day_wise['sunset']),
                    moonrise=datetime.datetime.fromtimestamp(day_wise['moonrise']),
                    moonset= datetime.datetime.fromtimestamp(day_wise['moonset']),
                    pressure= day_wise['pressure'],
                    humidity= day_wise['humidity'],
                    wind_speed= day_wise['wind_speed'],
                    wind_deg= day_wise['wind_deg'],
                    wind_gust= day_wise['wind_gust'],
                    weather= day_wise['weather'][0]['main'],
                    temp_min = day_wise['temp']['min'],
                    temp_max = day_wise['temp']['max'],
                    temp_day = day_wise['temp']['day'],
                    temp_night = day_wise['temp']['night'],
                    temp_evening = day_wise['temp']['eve'],
                    temp_morning = day_wise['temp']['morn']
                )
            )
        if city_weather_values:
            models.CityWeather.objects.bulk_create(city_weather_values)




