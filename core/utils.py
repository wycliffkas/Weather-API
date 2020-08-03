import pandas as pd
import numpy as np
import requests
from typing import List


def load_data(city: str, start_date: str, end_date: str):
    """Return weather data for a given city and time period
    Args:
        city (str): name of city
        start_date (str): date string of the start date for the time period
        end_date (str): date string of the end date for the time peroid
    Returns:
        weather_data (List): returns a list of weather data
    """

    url = f"http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=91ef5fcc4cd043148e4194112203007&q={city}&format=json&date={start_date}&enddate={end_date}"

    response = requests.get(url=url)

    data = response.json()

    weather_data = data["data"].get("weather")
    
    return weather_data


def get_weather_info(weather_data: List[dict]):
    """Returns a list computed weather information
        weather_data (List): a list of collected weather data.
    Returns:
        weather_info (List): returns a list of computed weather info.
    """

    weather_info = [{"date": data["date"], "max_temp_C": float(data["maxtempC"]), "max_temp_F": float(data["maxtempF"]),
                     "min_temp_C": float(data["mintempC"]), "min_temp_F": float(data["mintempF"]), "avg_temp_C": float(data["avgtempC"]),
                     "avg_temp_F": float(data["avgtempF"]), "max_humidity": np.max([float(h["humidity"]) for h in data["hourly"]]),
                     "min_humidity": np.min([float(h["humidity"]) for h in data["hourly"]]),
                     "avg_humidity": np.mean([float(h["humidity"]) for h in data["hourly"]])
                    }
                    for data in weather_data]
    
    return weather_info


def generate_df(weather_info: List[dict]):
    """Return pandas dataframe of the given weather information
    Args:
        weather_info (List): a list of computed weather information
    Returns:
        df (pd.DataFrame): returns pandas dataframe of the weather information
    """

    df = pd.DataFrame(weather_info)
    
    return df


def compute_statistics(df: pd.DataFrame):
    """Return computed aggregate of weather information statistics
    Args:
        df (pd.DataFrame): pandas dataframe of the weather information.
    Returns:
        computed_df: computed aggregate of weather information statistics.
    """

    computed_df = df.agg({'max_temp_C' : ['max'], 'max_temp_F' : ['max'], 'min_temp_C' : ['min'], 'min_temp_F' : ['min'],
            'avg_temp_C' : ['mean'], 'avg_temp_F' : ['mean'], 'max_humidity' : ['max'], 'min_humidity' : ['min'],
            'avg_humidity' : ['mean'],
           })
    
    return computed_df



if __name__ == "__main__":
    # load city data for a given period
    city = "Kampala"
    start_date = "2020-07-01"
    end_date = "2020-07-30"

    weather_data = load_data(city, start_date, end_date)

    # get weather info
    weather_info = get_weather_info(weather_data)

    # generate weather dataframe to be used to
    # compute statistics
    df = generate_df(weather_info)

    # compute required statics
    computed_df = compute_statistics(df)

    from pprint import pprint
    pprint(computed_df.to_dict(), indent=2)