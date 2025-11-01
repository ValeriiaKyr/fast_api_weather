from datetime import date, timedelta
import numpy as np
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# konfiguruje klienta API Open-Meteo z pamięcią podręczną (cache)
# oraz mechanizmem ponawiania zapytań w przypadku błędów
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# adres API Open-Meteo używany do pobierania prognozy pogody
URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_data(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None:
    """
    Pobiera dane pogodowe z API Open-Meteo dla określonej lokalizacji i zakresu dat

    Funkcja zwraca dane godzinowe: temperaturę, prędkość wiatru, wilgotność względną
    i zachmurzenie w postaci tablic numpy

    :param latitude: szerokość geograficzna lokalizacji
    :param longitude: długość geograficzna lokalizacji
    :param start_date: data początkowa w formacie YYYY-MM-DD
    :param end_date: data końcowa w formacie YYYY-MM-DD
    :return: krotka zawierająca dane pogodowe (temperatura, wiatr, wilgotność, chmury)
    """
    # definiuje parametry zapytania do API
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "temperature_2m",
            "wind_speed_10m",
            "relative_humidity_2m",
            "cloud_cover",
        ],
    }

    try:
        # wysyła zapytanie do API Open-Meteo
        responses = openmeteo.weather_api(URL, params=params)

        # wybiera pierwszą odpowiedź (API może zwrócić listę)
        response = responses[0]
        hourly = response.Hourly()

        # pobiera dane godzinowe dla poszczególnych zmiennych pogodowych
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(1).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()

        # zwraca dane w formie krotki (temperatura, wiatr, wilgotność, chmury)
        return (
            hourly_temperature_2m,
            hourly_wind_speed_10m,
            hourly_relative_humidity_2m,
            hourly_cloud_cover,
        )
    except Exception as e:
        # wyświetla błąd, jeśli nie udało się pobrać danych pogodowych
        print(f"[ERROR] Failed to fetch weather data for {latitude}, {longitude}: {e}")
        return None
