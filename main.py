import location_client
import weather_client
import searcher


def function_that_will_be_called_as_an_api_endpoint_from_the_front_end(origin, radius, sic_codes, weather_types):
    # todo - insert docstrings for this function
    # todo - add in try/catch to keep API from crashing from exceptions and to alert user of errors
    # If only one sic_code was passed, convert it to a single element list
    if isinstance(sic_codes, str):
        sic_codes = [sic_codes]
    # If only one weather_type was passed, convert it to a single element list
    if isinstance(weather_types, str):
        weather_types = [weather_types]

    # Get a list of all of the locations that match the sic_codes inside the search radius
    places_by_postal_code = location_client.location_search_grouped_by_postal_code(origin, radius, sic_codes)

    # Get a list of all unique postal codes we found
    postal_codes = list(places_by_postal_code.keys())

    # Get the weather forecast for each of these postal codes
    # dict: key => zip code, value => another dict, shown below
    # value dict: { "forecast": {weather forecast dict}, "match_count": int count of matches }
    weather_by_postal_code = {}
    for postal_code in postal_codes:
        forecast = weather_client.get_forecast_by_postal_code(postal_code)
        # Get the count of hours where the forecasted weather matches
        # If there were matches, add an entry to weather_by_postal_code
        matches = searcher.count_weather_matches(weather_types, forecast)
        if matches > 0:
            weather_by_postal_code[postal_code] = {
                'forecast': forecast,
                'match_count': matches
            }

    # For each of the places we found earlier, check if there were any matches for the
    # corresponding postal code. If there were, then add this place to the list of places being
    # returned as part of the response
    all_place_objects = []
    all_weather_forecasts = {}
    for postal_code in postal_codes:
        matched_postal_codes = list(weather_by_postal_code.keys())
        if postal_code not in matched_postal_codes:
            continue
        match_count = weather_by_postal_code[postal_code]['match_count']
        for place in places_by_postal_code[postal_code]:
            place['match_count'] = match_count
            place['postal_code'] = postal_code
            all_place_objects.append(place)
        forecast_list = weather_by_postal_code[postal_code]['forecast']
        all_weather_forecasts[postal_code] = forecast_list
    result = {
        "places": all_place_objects,
        "forecasts": all_weather_forecasts
    }
    print(result)
    return result




def main():
    origin = '98052'
    radius = '100'
    sic_codes = [581208]
    #sic_codes = [581208, '901006']
    weather_types = ['Sunny', 'Cloudy']

    function_that_will_be_called_as_an_api_endpoint_from_the_front_end(origin, radius, sic_codes, weather_types)


main()


def old_main_method():
    while True:
        origin = input('Search origin (single line address): ')
        radius = input('Search radius: ')
        destination_type = input('Destination Type: ')

        # todo - allow multiple destination types
        places_by_postal_code = location_client.group_places_by_postal_code(origin, radius, destination_type)
        if places_by_postal_code is None:
            continue

        search_filter = ['Sunny', 'Cloudy']

        # Each element of this list is a dict where the key is a
        # postal code and the value is the count of matches
        count_of_matches_per_postal_code = []
        postal_codes = list(places_by_postal_code.keys())
        for postal_code in postal_codes:
            location_key = weather_client.get_location_key(postal_code)
            if location_key is None:
                print('Error getting location key')
                continue

            # hourly_forecast is a list of dictionaries, where each dict
            # corresponds to the forecast for one hour
            hourly_forecast = weather_client.get_forecast(location_key)

            # Get a count of weather matches for this postal code
            # and store it in a dict where the key is the postal code
            # and the value is the count. Then append this dict to our list
            matches = searcher.count_weather_matches(search_filter, hourly_forecast)
            count_dict = {'postal_code': postal_code,
                          'count': matches}
            count_of_matches_per_postal_code.append(count_dict)

        count_of_matches_per_postal_code = [d for d in count_of_matches_per_postal_code if d['count'] > 0]

        # Sort the list of dictionaries by value (weather match count) in desc order
        count_of_matches_per_postal_code = sorted(count_of_matches_per_postal_code,
                                                  key=lambda x: x['count'],
                                                  reverse=True)

        # todo - link the count per zip code with the previous results of actual places
        print(count_of_matches_per_postal_code)
