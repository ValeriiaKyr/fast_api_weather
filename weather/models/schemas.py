from pydantic import BaseModel


class CityWeather(BaseModel):
    """
    Reprezentuje dane pogodowe dla konkretnego miasta wraz z obliczonym wynikiem pogodowym (score)

    Pola zawierają listy wartości dla danego okresu czasu (np. temperatury, prędkości wiatru itp.)
    """

    city: str
    country: str
    temperature: list
    wind_speed: list
    relative_humidity: list
    cloud_cover: list
    score: float
