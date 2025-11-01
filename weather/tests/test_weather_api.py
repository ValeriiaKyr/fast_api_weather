from datetime import date, timedelta
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from weather.api.v1.routes import router

# tworzy aplikację FastAPI i dołącza router z trasami API
app = FastAPI()
app.include_router(router)
client = TestClient(app)


@pytest.fixture
def mock_weather_data():
    """
    Tworzy przykładowe dane pogodowe używane w testach jako dane zwracane przez funkcję mockowaną
    """
    return (
        [10.5, 10.6, 11.0],  # temperatura
        [6.4, 3.7, 5.3],  # prędkość wiatru
        [69, 77, 80],  # wilgotność względna
        [100, 90, 80],  # zachmurzenie
    )


@patch("weather.api.v1.routes.get_weather_data")
@patch("weather.api.v1.routes.total_score")
def test_get_city_list(mock_total_score, mock_get_weather_data, mock_weather_data):
    """
    Testuje endpoint /cities-scores/ bez podania dat
    Sprawdza, czy zwracane dane mają prawidłową strukturę i typy
    oraz czy wywołania funkcji pomocniczych następują oczekiwaną liczbę razy
    """
    # ustawia wartości zwracane przez mockowane funkcje
    mock_get_weather_data.return_value = mock_weather_data
    mock_total_score.return_value = 1.23

    # wysyła zapytanie GET do endpointu
    response = client.get("/cities-scores/")
    assert response.status_code == 200

    # parsuje odpowiedź jako JSON
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 6  # liczba miast powinna wynosić 6

    # sprawdza obecność wymaganych kluczy w pierwszym obiekcie
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
        assert key in first, f"Brak klucza {key}"

    # sprawdza typy danych
    assert isinstance(first["city"], str)
    assert isinstance(first["country"], str)
    assert isinstance(first["temperature"], list)
    assert isinstance(first["wind_speed"], list)
    assert isinstance(first["relative_humidity"], list)
    assert isinstance(first["cloud_cover"], list)
    assert isinstance(first["score"], (int, float))

    # sprawdza poprawność wartości score
    assert 0 <= first["score"] <= 10

    # weryfikuje liczbę wywołań funkcji pomocniczych
    assert mock_get_weather_data.call_count == 6
    assert mock_total_score.call_count == 6

    # sprawdza, czy używana data to wczorajszy dzień
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    for call in mock_get_weather_data.call_args_list:
        args, kwargs = call
        start = args[2]
        assert start == yesterday, f"Oczekiwano daty {yesterday}, otrzymano {start}"


@patch("weather.api.v1.routes.get_weather_data")
@patch("weather.api.v1.routes.total_score")
def test_get_city_list_with_dates(
    mock_total_score, mock_get_weather_data, mock_weather_data
):
    """
    Testuje endpoint /cities-scores/ z przekazanymi parametrami start_date i end_date
    Sprawdza, czy zwracane dane mają odpowiednią strukturę
    """
    mock_get_weather_data.return_value = mock_weather_data
    mock_total_score.return_value = 2.34

    # ustawia daty początkową i końcową na dzisiejszy dzień
    start = end = date.today().isoformat()

    # wysyła zapytanie GET z parametrami dat
    response = client.get(f"/cities-scores/?start_date={start}&end_date={end}")
    assert response.status_code == 200

    # sprawdza strukturę danych odpowiedzi
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 6
    assert all("city" in item and "score" in item for item in data)


@patch("weather.api.v1.routes.get_weather_data")
def test_get_city_list_with_error(mock_get_weather_data):
    """
    Testuje sytuację, w której zewnętrzne API (Open-Meteo)
    zwraca niepoprawne lub nietypowe dane pogodowe — w tym przypadku same zera.
    Celem testu jest upewnienie się, że endpoint nie zgłasza błędu
    i poprawnie zwraca odpowiedź HTTP 200 z prawidłową strukturą JSON.
    """

    # imitujemy dane pogodowe zawierające same zera
    mock_get_weather_data.return_value = (
        [0.0] * 5,  # temperatura
        [0.0] * 5,  # prędkość wiatru
        [0.0] * 5,  # wilgotność względna
        [0.0] * 5,  # zachmurzenie
    )

    # wysyłamy żądanie GET do endpointu
    response = client.get("/api/v1/cities-scores/")

    # sprawdzamy, że odpowiedź zakończyła się sukcesem (status 200)
    assert response.status_code == 200

    # parsujemy dane odpowiedzi w formacie JSON
    data = response.json()

    # upewniamy się, że zwrócono listę obiektów
    assert isinstance(data, list)
    assert len(data) > 0

    # sprawdzamy, że każdy obiekt ma klucz "score" i że jego wartość jest liczbą
    for city in data:
        assert "score" in city
        assert isinstance(city["score"], (int, float))
