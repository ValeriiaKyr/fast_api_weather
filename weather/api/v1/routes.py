from datetime import date, timedelta

import numpy as np
from fastapi import APIRouter, Query

from weather.models.schemas import CityWeather
from weather.services.weather_service import get_weather_data
from weather.utils.metrics import total_score

router = APIRouter()

CITIES = [
    ["Warsaw", "Poland", (52.2297, 21.0122)],
    ["Gdansk", "Poland", (54.3520, 18.6466)],
    ["Berlin", "Germany", (52.5200, 13.4050)],
    ["Krakow", "Poland", (50.0647, 19.9450)],
    ["Nurnberg", "Germany", (49.4521, 11.0767)],
    ["Munich", "Germany", (48.1351, 11.5820)],
]


def to_list(arr):
    if isinstance(arr, np.ndarray):
        return arr.tolist()
    return arr


@router.get("/cities-scores/", response_model=list[CityWeather])
def get_city_list(start_date: str = Query(None), end_date: str = Query(None)):
    if not start_date or not end_date:
        yesterday = date.today() - timedelta(days=1)
        start_date = end_date = yesterday.isoformat()

    results = []
    for city, country, (lat, lon) in CITIES:
        temp, speed, humidity, cloud = get_weather_data(lat, lon, start_date, end_date)

        temp = to_list(temp)
        speed = to_list(speed)
        humidity = to_list(humidity)
        cloud = to_list(cloud)
        score = total_score(temp, speed, humidity, cloud)
        results.append(
            CityWeather(
                city=city,
                country=country,
                temperature=temp,
                wind_speed=speed,
                relative_humidity=humidity,
                cloud_cover=cloud,
                score=score,
            )
        )
    return sorted(results, key=lambda x: x.score, reverse=True)
