from collections import defaultdict

import http_client
import settings

url = settings.mapquest_radius_search_url
api_key = settings.mapquest_api_key


def group_places_by_postal_code(origin, radius, sic_code):
    params = {
        'origin': origin,
        'radius': radius,
        'hostedData': f'mqap.ntpois|group_sic_code=?|{sic_code}',
        'key': api_key,
        'maxMatches': settings.mapquest_max_matches,
        'unit': settings.mapquest_radius_search_unit
    }

    # Query the location API
    response = http_client.get_request(url, params=params)
    # todo - handle ambiguous results (try sending 33432 as the location

    # If there are any errors, they'l be in the messages dict inside info
    info = response.get('info')
    messages = info.get('messages') if info is not None else None
    # if messags is not None, there was an error, get the details
    if messages is not None and len(messages) > 0:
        messages_string = ''
        for message in messages:
            fixed_message = message.replace('[', '').replace(']', '')
            messages_string = f'{fixed_message}, '
        messages_string = messages_string[:-2]
        print(f'Error: {messages_string}')
        return None

    # List of search results from API
    search_results = response.get('searchResults')

    # If there were no results for search parameters, return
    # an empty dictionary
    if search_results is None or len(search_results) == 0:
        return {}


    # Get data from each of the search results and add it to
    # the places_by_postal_code dict
    places_by_postal_code = {}
    for result in search_results:
        # Fields dictionary holds most of the relevant data for this place
        # If it's None, then continue to the next result
        fields = result.get('fields')
        if fields is None:
            continue

        # If postal_code is None for any reason, continue to next result
        postal_code = fields.get('postal_code')
        if postal_code is None:
            continue

        # Create a dictionary to hold all of the data for this search result
        place = {
            'name': result.get('name'),
            'lat': fields.get('lat'),
            'lng': fields.get('lng'),
            'distance': result.get('distance'),
            'destination_type': settings.destination_types_by_sic_code.get(sic_code)
        }

        # If this postal code exists in the places_by_postal_code dict
        # already, then get the list and append this place to it
        # Else, create a new list and add it to the dict
        if postal_code in places_by_postal_code:
            place_list = places_by_postal_code[postal_code]
            place_list.append(place)
            places_by_postal_code[postal_code] = place_list
        else:
            places_by_postal_code[postal_code] = [place]

    # Return the search results
    return places_by_postal_code


def location_search_grouped_by_postal_code(origin, radius, sic_codes):
    """
    Queries the location APIs to find matching places of interest
    # todo - use the below syntax for parameters - look it up when you have internet
    :parameter
    Parameters:
       origin (string): The origin to start searching at, this can be either a zip code,
                        a lat/lon pair, a city, or a full address
       radius (int): The search radius, in miles
       sic_codes(list): the sic_code or sic_codes to search for
    # todo - use the below syntax for return type - look it up when you have internet
    :returns places_by_postal_code:
    """
    places_by_postal_code = {}
    for sic_code in sic_codes:
        # Query the API to retrieve matches for the origin, radius, and sic_code provided
        search_results = group_places_by_postal_code(origin, radius, sic_code)

        # todo - if there was an error getting location data, search_reuslts will be None, handle that error
        if search_results is None:
            pass

        # Append these results to the places_by_postal_code dict
        postal_codes = list(search_results.keys())
        for postal_code in postal_codes:
            if postal_code not in places_by_postal_code.keys():
                # Add the list of places from the search result
                # to the places_by_postal_code dict
                places_by_postal_code[postal_code] = search_results[postal_code]
            else:
                # Get the existing list from places_by_postal_code and append the search results, then place it back
                existing_list = places_by_postal_code[postal_code]
                results_list = search_results[postal_code]
                existing_list.extend(results_list)
                # Turn it into a set and then back to a list to get rid of duplicates
                existing_list = list(set(existing_list))
                places_by_postal_code[postal_code] = existing_list
    return places_by_postal_code