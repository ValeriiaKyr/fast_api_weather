from datetime import date, timedelta
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from weather.api.v1.routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


@pytest.fixture
def mock_weather_data():
    return (
        [10.5, 10.6, 11.0],  # temperature
        [6.4, 3.7, 5.3],  # wind_speed
        [69, 77, 80],  # relative_humidity
        [100, 90, 80],  # cloud_cover
    )


@patch("weather.api.v1.routes.get_weather_data")
@patch("weather.api.v1.routes.total_score")
def test_get_city_list(mock_total_score, mock_get_weather_data, mock_weather_data):
    mock_get_weather_data.return_value = mock_weather_data
    mock_total_score.return_value = 1.23

    response = client.get("/cities-scores/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 6

    first = data[0]
    for key in [
        "city",
        "country",
        "temperature",
        "wind_speed",
        "relative_humidity",
        "cloud_cover",
        "score",
    ]:
        assert key in first, f"Key {key} is missing"

    assert isinstance(first["city"], str)
    assert isinstance(first["country"], str)
    assert isinstance(first["temperature"], list)
    assert isinstance(first["wind_speed"], list)
    assert isinstance(first["relative_humidity"], list)
    assert isinstance(first["cloud_cover"], list)
    assert isinstance(first["score"], (int, float))

    assert 0 <= first["score"] <= 10

    assert mock_get_weather_data.call_count == 6
    assert mock_total_score.call_count == 6

    yesterday = (date.today() - timedelta(days=1)).isoformat()
    for call in mock_get_weather_data.call_args_list:
        args, kwargs = call
        start = args[2]
        assert start == yesterday, f"Expected date {yesterday}, received {start}"


@patch("weather.api.v1.routes.get_weather_data")
@patch("weather.api.v1.routes.total_score")
def test_get_city_list_with_dates(
    mock_total_score, mock_get_weather_data, mock_weather_data
):
    mock_get_weather_data.return_value = mock_weather_data
    mock_total_score.return_value = 2.34

    start = end = date.today().isoformat()
    response = client.get(f"/cities-scores/?start_date={start}&end_date={end}")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 6
    assert all("city" in item and "score" in item for item in data)
