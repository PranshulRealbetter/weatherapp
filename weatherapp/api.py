from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
import json
from django.core.cache import cache
from datetime import timedelta, datetime

def build_redirect_url(**kwargs):
    url = kwargs.get('url')
    params = kwargs.get('params')
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string
    return response

class WeatherDataFetcher:
    def __init__(self, city_name, *args, **kwargs):
        self.city_name = city_name

    def fetch_data(self):
        cached_data = cache.get(self.city_name)

        if cached_data:
            print('Cache hit')
            return json.loads(cached_data)
        
        print('Cache miss, making API call...')
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={self.city_name}&appid={settings.API_KEY}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'list' in data:
                now = datetime.now()
                midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                timeout = (midnight - now).total_seconds()
                cache.set(self.city_name, json.dumps(data['list']), timeout=timeout)
                return data['list']
        
        return None
