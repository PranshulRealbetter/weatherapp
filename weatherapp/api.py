from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
import json
import redis
from django.core.cache import cache
from datetime import timedelta, datetime
from functools import wraps
import time
from weatherapp.serializers import WeatherForecastSerializer

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start timing
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.perf_counter()  # End timing
        total_time = end_time - start_time  # Calculate elapsed time
        print(
            f"Function {func.__name__}{args} {kwargs} took {total_time * 1000:.4f} milliseconds"  # , result: {result}"
        )
        return result  # Return the result of the function

    return timeit_wrapper


def build_redirect_url(**kwargs):
    url = kwargs.get("url")
    params = kwargs.get("params")
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response["Location"] += "?" + query_string
    return response


class WeatherDataFetcher:
    def __init__(self, *args, **kwargs):
        self.query = kwargs.get("query")

    @timeit
    def fetch_data(self):
        cached_data = cache.get(self.query)
        if cached_data:
            # TODO: Add logging
            print("cache hit")
            # print(json.loads(cached_data))
            return json.loads(cached_data)
          # TODO: Add logging
        # print("cache miss, making api call again")
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={self.query}&appid={settings.API_KEY}"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            if "list" in data:
                serializer = WeatherForecastSerializer(data["list"], many=True)
                serialized_data = serializer.data
                now = datetime.now()
                midnight = (now + timedelta(days=1)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                timeout = (midnight - now).total_seconds()
                cache.set(self.query, json.dumps(serialized_data), timeout=timeout)
                return serialized_data
        return None
