from pydantic import BaseModel

class CityWeather(BaseModel):
    city: str
    country: str
    temperature: list 
    wind_speed: list
    relative_humidity: list
    cloud_cover: list
    score: float
