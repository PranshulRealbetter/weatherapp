from django.shortcuts import render, reverse, redirect
from django.conf import settings
from .serializers import WeatherForecastSerializer
from .api import WeatherDataFetcher, build_redirect_url

def home(request):
    if request.method == 'POST':
        query = request.POST.get('query', None)
        if query:
            return build_redirect_url(url='weatherapp:forecast_results', params={'query': query})
    return render(request, 'index.html', {})

def forecast_results(request):
    query = request.GET.get('query', None)
    if query:
        weather_data = WeatherDataFetcher(city_name=query).fetch_data()  
        if weather_data:
            serializer = WeatherForecastSerializer(weather_data, many=True)
            forecast_results = serializer.data

            context = {
                'results': forecast_results,
                'query': query,
            }
            return render(request, 'results.html', context)

    return redirect(reverse('weatherapp:home'))
