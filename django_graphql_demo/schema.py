import graphene
from datetime import datetime, timedelta
from graphene_django import DjangoObjectType

from weather.models import City, CityWeather


class CityType(DjangoObjectType):
    class Meta:
        model = City
        fields = ("id", "name", "state", "country", "latitude", "longitude")


class Query(graphene.ObjectType):
    all_cities = graphene.List(CityType)
    city_by_name = graphene.Field(CityType, name=graphene.String(required=True))
    city_by_country = graphene.List(CityType, country=graphene.String(required=True))

    def resolve_all_cities(root, info):
        return City.objects.all()

    def resolve_city_by_name(root, info, name):
        try:
            print(info)
            return City.objects.get(name=name)
        except City.DoesNotExist:
            return None

    def resolve_city_by_country(root, info, country):
        try:
            print(info)
            return City.objects.filter(country=country)
        except City.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)


class CityWeatherType(DjangoObjectType):
    class Meta:
        model = CityWeather
        fields = "__all__"


class CityWeatherQuery(graphene.ObjectType):
    get_weather_by_city = graphene.List(CityWeatherType, city_name=graphene.List(graphene.String),
                                        day_diff=graphene.String(required=True))
    get_weather_by_city_and_type = graphene.List(CityWeatherType, city_name=graphene.List(graphene.String),
                                                 weather_type=graphene.List(graphene.String),
                                                 day_diff=graphene.String(required=True))

    def resolve_get_weather_by_city(root, info, city_name, day_diff):
        try:
            if int(day_diff) > 7:
                raise Exception("Please enter day diff between 0-7")

            cities = City.objects.filter(name__in=city_name)
            search_date = datetime.now() + timedelta(days=int(day_diff))
            return CityWeather.objects.get_weather_details(cities, search_date.date())
        except CityWeather.DoesNotExist:
            return None

    def resolve_get_weather_by_city_and_type(root, info, city_name, weather_type, day_diff):
        try:
            if int(day_diff) > 7:
                raise Exception("Please enter day diff between 0-7")
            cities = City.objects.filter(name__in=city_name)
            search_date = datetime.now() + timedelta(days=int(day_diff))
            return CityWeather.objects.get_weather_by_type(cities, search_date.date(), weather_type)
        except CityWeather.DoesNotExist:
            return None


class HottestCityWeatherQuery(graphene.ObjectType):
    get_hottest_cities = graphene.List(CityWeatherType, city_name=graphene.List(graphene.String),
                                       day_diff=graphene.String(required=True))

    def resolve_get_hottest_cities(root, info, city_name, day_diff):
        try:
            if int(day_diff) > 7:
                raise Exception("Please enter day diff between 0-7")

            cities = City.objects.filter(name__in=city_name)
            search_date = datetime.now() + timedelta(days=int(day_diff))
            return CityWeather.objects.get_hottest_cities(cities, search_date.date())
        except CityWeather.DoesNotExist:
            return None

city_weather_schema = graphene.Schema(query=CityWeatherQuery)
hottest_cities_schema = graphene.Schema(query=HottestCityWeatherQuery)
