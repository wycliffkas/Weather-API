from django.urls import path

from .views import get_weather_statistics_view


urlpatterns = [
    path("statistics/", get_weather_statistics_view, name="statistics"),
]

