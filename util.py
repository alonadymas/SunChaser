from base64 import b64encode

import settings


def basic_auth_header(username, password):
    encoded_credentials = b64encode(bytes(f"{username}:{password}", encoding="ascii")).decode("ascii")
    return {
        "Authorization": f"Basic {encoded_credentials}"
    }


def normalize_weather_types(weather_type):
    # API can return NULL weather types,
    # so normalize None to 'Undefined'
    if weather_type is None:
        return 'Undefined'

    # If weather type is in the mapping dictionary, return the mapped result
    # Else return an empty string
    weather_type_dict = settings.accuweather_weather_types
    if weather_type.lower() in weather_type_dict:
        return weather_type_dict[weather_type.lower()]
    else:
        return weather_type
