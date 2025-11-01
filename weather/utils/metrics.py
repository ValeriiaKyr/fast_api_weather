def get_average_value(values):
    """
    Oblicza średnią wartość z listy liczb

    :param values: lista wartości liczbowych
    :return: średnia arytmetyczna
    """
    avg = sum(values) / len(values)
    return avg


def score_temperature(temp: float) -> float:
    """
    Oblicza wynik dla temperatury
    wartość idealna to 24°C, a odchylenie obniża wynik

    :param temp: średnia temperatura
    :return: wynik w zakresie 0–10
    """
    return max(0, 10 - abs(temp - 24))


def score_wind_speed(speed: float) -> float:
    """
    Oblicza wynik dla prędkości wiatru
    Im mniejsza prędkość, tym wyższy wynik (maks. 10)

    :param speed: średnia prędkość wiatru
    :return: wynik w zakresie 0–10
    """
    return max(0, 10 - speed)


def score_humidity(humidity: float) -> float:
    """
    Oblicza wynik dla wilgotności względnej
    Idealna wartość to około 50%, odchylenia obniżają wynik

    :param humidity: średnia wilgotność względna
    :return: wynik w zakresie 0–10
    """
    return max(0, 10 - abs(humidity - 50) / 5)


def score_cloud_cover(cloud: float) -> float:
    """
    Oblicza wynik dla zachmurzenia
    Najlepszy wynik uzyskuje się przy 25% zachmurzenia

    :param cloud: średnie zachmurzenie w %
    :return: wynik w zakresie 0–10
    """
    return max(0, 10 - abs(cloud - 25) / 2.5)


def total_score(
    temp: list[float],
    speed: list[float],
    humidity: list[float],
    cloud: list[float],
) -> float:
    """
    Oblicza łączny wynik pogodowy (score) na podstawie czterech czynników:
    temperatury, prędkości wiatru, wilgotności i zachmurzenia.
    Każdemu czynnikowi przypisana jest waga:
    - temperatura: 35%
    - wiatr: 20%
    - wilgotność: 20%
    - zachmurzenie: 25%

    :param temp: lista temperatur
    :param speed: lista prędkości wiatru
    :param humidity: lista wilgotności względnej
    :param cloud: lista zachmurzenia
    :return: łączny wynik pogodowy w zakresie 0–10
    """
    temp_s = score_temperature(get_average_value(temp))
    speed_s = score_wind_speed(get_average_value(speed))
    humidity_s = score_humidity(get_average_value(humidity))
    cloud_s = score_cloud_cover(get_average_value(cloud))

    return temp_s * 0.35 + speed_s * 0.2 + humidity_s * 0.2 + cloud_s * 0.25
