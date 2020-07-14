# ==========================
# API Settings
# ==========================
chase_weather_body_required_fields = ['origin', 'radius', 'sic_codes', 'weather_types']
chase_weather_expected_data_types ={
    'origin': [str, int],
    'radius': [int, str, float],
    'sic_codes': [int, list, str],
    'weather_types': [str, list]
}
# ==========================
# Misc Settings
# ==========================
destination_types_by_sic_code = {
    581208: 'Restaurants',
    581301: 'Bars',
    581214: 'Cafes',
    799951: 'Parks',
    902209: 'Lakes/Ponds',
    701107: 'Bed & Breakfasts',
    703301: 'Campgrounds',
    581305: 'Pubs',
    901006: 'Beaches',
    999333: 'Tourist Attractions',
    842201: 'Zoos'
}

# ==========================
# MapQuest API Settings
# ==========================
mapquest_radius_search_url = 'http://www.mapquestapi.com/search/v2/radius'
mapquest_api_key = '4CsAxBC4kjsMfKA9oefJ9i61nI76aVMx'
mapquest_max_matches = 10
mapquest_radius_search_unit = 'dmin'
sic_codes = {
    'restaurants': 581208,
    'bars': 581301,
    'cafes': 581214,
    'parks': 799951,
    'Lakes_and_ponds': 902209,
    'bed_and_breakfasts': 701107,
    'campgrounds': 703301,
    'pubs': 581305,
    'beaches': 901006,
    'tourist_attractions': 999333,
    'zoos': 842201
}

# ==========================
# AccuWeather API Settings
# ==========================
accuweather_api_key = 'PfnnmdV3eTVo9vcqzesKMfr4VArzWST2'
accuweather_postal_code_search_url = 'http://dataservice.accuweather.com/locations/v1/postalcodes/search'
accuweather_forecast_search_url = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour'
accuweather_language = 'en-us'

# ==========================
# AccuWeather Weather Types
# ==========================
sunny_weather_type = 'Sunny'
rain_weather_type = 'Rainy'
snow_weather_type = 'Snow'
cloudy_weather_type = 'Cloudy'
accuweather_weather_types = {
    'sunny': sunny_weather_type,
    'mostly sunny': sunny_weather_type,
    'partly sunny': sunny_weather_type,
    'hazy sunshine': sunny_weather_type,
    'cloudy': cloudy_weather_type,
    'dreary (overcast)': cloudy_weather_type,
    'fog': cloudy_weather_type,
    'showers': rain_weather_type,
    'partly sunny w/ showers': rain_weather_type,
    't-storms': rain_weather_type,
    'partly sunny w/ t-storms': rain_weather_type,
    'rain': rain_weather_type,
    'flurries': snow_weather_type,
    'partly sunny w/ flurries': snow_weather_type,
    'snow': snow_weather_type,
    'ice': snow_weather_type,
    'sleet': snow_weather_type,
    'freezing rain': rain_weather_type,
    'rain and snow': rain_weather_type,
    'partly cloudy': cloudy_weather_type,
    'intermittent clouds': cloudy_weather_type,
    'mostly cloudy': cloudy_weather_type,
    'partly cloudy w/ showers': rain_weather_type,
    'mostly cloudy w/ showers': rain_weather_type,
    'partly cloudy w/ t-storms': rain_weather_type,
    'mostly cloudy w/ t-storms': rain_weather_type,
    'mostly cloudy w/ flurries': snow_weather_type,
    'mostly cloudy w/ snow': snow_weather_type
}