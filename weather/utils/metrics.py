def get_average_value(values):
    avg = sum(values) / len(values)
    return avg


def score_temperature(temp: float) -> float:
    return max(0, 10 - abs(temp - 24))


def score_wind_speed(speed: float) -> float:
    return max(0, 10 - speed)


def score_humidity(humidity: float) -> float:
    return max(0, 10 - abs(humidity - 50) / 5)


def score_cloud_cover(cloud: float) -> float:
    if cloud <= 25:
        return max(0, 10 - abs(cloud - 25) / 2.5)
    return max(0, 10 - abs(cloud - 25) / 7.5)


def total_score(temp, speed, humidity, cloud):
    temp_s = score_temperature(get_average_value(temp))
    speed_s = score_wind_speed(get_average_value(speed))
    humidity_s = score_humidity(get_average_value(humidity))
    cloud_s = score_cloud_cover(get_average_value(cloud))

    return temp_s * 0.35 + speed_s * 0.2 + humidity_s * 0.2 + cloud_s * 0.25
