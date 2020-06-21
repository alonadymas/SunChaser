import location_client
import weather_client
import weather_searcher

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
        matches = weather_searcher.count_weather_matches(search_filter, hourly_forecast)
        count_dict = {'postal_code': postal_code,
                      'count': matches}
        count_of_matches_per_postal_code.append(count_dict)

    # todo - test the filtering functionality
    count_of_matches_per_postal_code = [d for d in count_of_matches_per_postal_code if d['count'] > 0]

    # Sort the list of dictionaries by value (weather match count) in desc order
    count_of_matches_per_postal_code = sorted(count_of_matches_per_postal_code,
                                              key=lambda x: x['count'],
                                              reverse=True)

    # todo - link the count per zip code with the previous results of actual places
    print(count_of_matches_per_postal_code)
