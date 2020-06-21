def count_weather_matches(search_filter, forecast_list):
    # If search_filter is just a string, convert it to a list
    if isinstance(search_filter, str):
        search_filter = [search_filter]

    count = 0
    # Check each hour of the hourly forecast
    # If the weather type matches our search filter, then increment count
    for forecast in forecast_list:
        weather_type = forecast.get('weather_type')
        if weather_type in search_filter:
            count += 1

    # Return count of matches
    return count
