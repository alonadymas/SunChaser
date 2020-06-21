import time

import requests
from requests import HTTPError


def get_request(url, headers=None, params=None, max_retry=0):
    response = requests.get(url=url, params=params, headers=headers)

    # If we received a server error, retry the request until we hit max_retry limit
    status_code = response.status_code
    retry_count = 0
    retry_wait = 30
    while status_code in range(500, 599) and retry_count < max_retry:
        retry_count += 1
        # Waiting time grows after each retry
        time.sleep(retry_wait * retry_count)
        response = requests.get(url=url, params=params, headers=headers)
        status_code = response.status_code

    # todo - non success HTTP status code shouldn't raise an exception, return the status code and response details
    # If status code isn't 2XX, there was an error, raise HTTPError exception
    if status_code not in range(200, 299):
        raise HTTPError(f"Error code {response.status_code} when making request to {url} "
                        f"with headers:{headers} and params: {params}")

    return response.json()
