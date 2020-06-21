import http_client
import settings
import util

postal_code_search_url = settings.accuweather_postal_code_search_url
forecast_search_url = settings.accuweather_forecast_search_url
accuweather_api_key = settings.accuweather_api_key
accuweather_language = settings.accuweather_language


def get_location_key(postal_code):
    params = {
        'apikey': accuweather_api_key,
        'q': postal_code,
        'language': accuweather_language
    }

    # Query the weather API
    response = http_client.get_request(postal_code_search_url, params=params)

    if response is None or len(response) < 1:
        return None

    # Return the location key from weather API
    return response[0].get('Key')


def get_forecast(location_key):
    # Append location key to forecast_search_url
    full_url = f'{forecast_search_url}/{location_key}'

    params = {
        'apikey': accuweather_api_key,
        'language': accuweather_language
    }

    # Query the weather API
    response = http_client.get_request(full_url, params=params)

    # Aggregate the data
    weather_result = []
    # For each hourly result, get the relevant data, create a dictionary
    # to hold the data and append it to the weather_result list
    for result in response:
        dt = result.get('DateTime')
        weather_type = result.get('IconPhrase')
        weather_type = util.normalize_weather_types(weather_type)
        rain_chance = result.get('PrecipitationProbability')
        temp_value = result.get('Temperature').get('Value')
        temp_unit = result.get('Temperature').get('Unit')

        result_dict = {
            'datetime': dt,
            'weather_type': weather_type,
            'rain_chance': rain_chance,
            'temp': {
                'value': temp_value,
                'unit': temp_unit
            }
        }
        weather_result.append(result_dict)

    # Return the list of dicts, where each dict corresponds to the
    # weather forecast for one hour
    return weather_result
