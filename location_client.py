from collections import defaultdict

import http_client
import settings

url = settings.mapquest_radius_search_url
api_key = settings.mapquest_api_key


def group_places_by_postal_code(origin, radius, destination_type):
    # todo - fix this mapping
    # Get the destination_code corresponding to the entered location type
    destination_code = settings.sic_codes.get(destination_type.lower().replace(' ', '_'))

    # If invalid destination type was entered, return None
    if destination_code is None:
        print('Invalid destination type')
        return None

    params = {
        'origin': origin,
        'radius': radius,
        'hostedData': f'mqap.ntpois|group_sic_code=?|{destination_code}',
        'key': api_key,
        'maxMatches': settings.mapquest_max_matches,
        'unit': settings.mapquest_radius_search_unit
    }

    # Query the location API
    response = http_client.get_request(url, params=params)

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
            'distance': result.get('distance')
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
