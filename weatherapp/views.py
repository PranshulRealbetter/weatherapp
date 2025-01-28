from django.shortcuts import render, reverse, redirect
from django.conf import settings

from .api import ApiCall,redirecturl

def index(request):
    if request.method=='POST':
        query=request.POST.get('query',None)
        if query:
            return redirecturl(url='weatherapp:results',params={'query':query})
    return render(request, 'index.html',{})

def results(request):
    query= request.GET.get('query',None)
    if query:
        results=ApiCall(query=query).get_data()
        if results:
            simple_results=[]
            for forecast in results:
                simple_results.append({
                    'date':forecast['dt'],
                    'temperature':forecast['main']['temp'],
                    'feels_like':forecast['main']['feels_like'],
                    'humidity': forecast['main']['humidity'],
                    'weather': forecast['weather'][0]['description'],
                    'wind_speed': forecast['wind']['speed'],
                })


            context={
                'results':simple_results,
                'query':query,
            } 

            return render(request, 'results.html',context)
            
    return redirect(reverse('weatherapp:home'))

# Create your views here.
