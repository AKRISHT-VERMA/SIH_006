import requests


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "rain"
        ),
        "hourly": (
            "precipitation,"
            "precipitation_probability,"
            "rain"
        ),
        "forecast_days": 3,
        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_rainfall_forecast(latitude, longitude):

    weather = get_weather(
        latitude,
        longitude
    )

    precipitation = weather["hourly"]["precipitation"]

    probability = weather["hourly"]["precipitation_probability"]

    next_24_hours = precipitation[:24]

    next_24_probability = probability[:24]

    total_rain = sum(next_24_hours)

    maximum_probability = max(next_24_probability)

    return {
        "rainfall_next_24h": round(total_rain, 2),
        "max_rain_probability": maximum_probability
    }


# ============================================
# TEST
# ============================================

if __name__ == "__main__":

    latitude = 25.0054
    longitude = 96.3691

    weather = get_weather(
        latitude,
        longitude
    )

    print()
    print("WEATHER TEST")
    print("====================")

    print(
        "Temperature:",
        weather["current"]["temperature_2m"],
        "°C"
    )

    print(
        "Humidity:",
        weather["current"]["relative_humidity_2m"],
        "%"
    )

    print(
        "Precipitation:",
        weather["current"]["precipitation"],
        "mm"
    )

    print(
        "Rain:",
        weather["current"]["rain"],
        "mm"
    )

    forecast = get_rainfall_forecast(
        latitude,
        longitude
    )

    print()
    print("RAINFALL FORECAST")
    print("====================")

    print(
        "Rainfall next 24 hours:",
        forecast["rainfall_next_24h"],
        "mm"
    )

    print(
        "Maximum rain probability:",
        forecast["max_rain_probability"],
        "%"
    )