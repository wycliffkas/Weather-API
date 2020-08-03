import json

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response


from core import (load_data, get_weather_info, generate_df, compute_statistics)


@api_view()
def get_weather_statistics_view(request):
    """api view to return computed weather statistics"""
    
    get_data = request.GET
    
    city = get_data.get("city", "Kampala")
    start_date = get_data.get("start_date", "2020-01-01")
    end_date = get_data.get("end_date", "2020-01-31")

    # load city data for a given period
    weather_data = load_data(city, start_date, end_date)

    # get weather info
    weather_info = get_weather_info(weather_data)

    # generate weather dataframe to be used to
    # compute statistics
    df = generate_df(weather_info)

    # compute required statics
    computed_df = compute_statistics(df)
    statistics = computed_df.to_dict()
    
    stat_data = {
        "max_tempC": statistics["max_temp_C"]["max"],
        "max_tempF": statistics["max_temp_F"]["max"],
        "min_tempC": statistics["min_temp_C"]["min"],
        "min_tempF": statistics["min_temp_C"]["min"],
        "avg_tempC": statistics["avg_temp_C"]["mean"],
        "avg_tempF": statistics["avg_temp_F"]["mean"],
        "max_humidity": statistics["max_humidity"]["max"],
        "min_humidity": statistics["min_humidity"]["min"],
        "avg_humidity": statistics["avg_humidity"]["mean"]
    }

    return Response(data=stat_data)
