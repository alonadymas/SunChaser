import flask
from flask import request, jsonify

import location_client
import searcher
import settings
import weather_client

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/chaseWeather', methods=['POST'])
def home():
    a = request
    # Try getting the body of the request as JSON
    try:
        request_body = request.get_json()
        if request_body is None:
            # todo - return an error response
            return "No body in request"
        # Verify that all of the required fields are present in the body of the request and that the data schema matches
        required_fields = settings.chase_weather_body_required_fields
        for required_field in required_fields:
            if request_body.get(required_field) is None:
                # todo - return an error response
                return "Missing Field(s)"
            request_field = request_body[required_field]
            if type(request_field) not in settings.chase_weather_expected_data_types[required_field]:
                # todo - return an error response
                return "Invalid data"
        print(request_body)
    # Todo - identify actual exceptions and handle them, such as invalid json exception
    except Exception as e:
        print(e.with_traceback())

    # At this point, it's guaranteed that all of these values are not None
    origin = request_body['origin']
    radius = request_body['radius']
    sic_codes = request_body['sic_codes']
    weather_types = request_body['weather_types']

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
    return jsonify(result)

app.run()