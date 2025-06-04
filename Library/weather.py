"""Hämta och visa aktuellt väder för en angiven stad."""

import os
import sys
from typing import Tuple

import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str, api_key: str) -> Tuple[float, str]:
    """Returnerar temperatur och väderbeskrivning för ``city``.

    :param city: Stadens namn.
    :param api_key: API-nyckeln för OpenWeatherMap.
    :return: ``(temperatur, beskrivning)`` där temperaturen är i Celsius.
    :raises ValueError: Om staden inte finns.
    :raises PermissionError: Om API-nyckeln är ogiltig.
    :raises requests.RequestException: Vid nätverksfel eller andra HTTP-fel.
    """

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "sv",
    }
    resp = requests.get(API_URL, params=params, timeout=10)
    if resp.status_code == 404:
        raise ValueError("Staden hittades inte.")
    if resp.status_code == 401:
        raise PermissionError("Ogiltig API-nyckel.")
    resp.raise_for_status()
    data = resp.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"].capitalize()
    return temp, desc

def main() -> None:
    """Startar det interaktiva väderprogrammet."""

    city = input("Ange stadens namn: ").strip()
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        print(
            "Saknar API-nyckel. Ange den i miljövariabeln OPENWEATHER_API_KEY."
        )
        sys.exit(1)
    try:
        temp, desc = get_weather(city, api_key)
        print(f"Vädret i {city} är {desc} med {temp:.1f} °C")
    except (ValueError, PermissionError) as e:
        print(e)
    except requests.RequestException as e:
        print(f"Fel vid anslutning till vädertjänsten: {e}")

if __name__ == "__main__":
    main()
