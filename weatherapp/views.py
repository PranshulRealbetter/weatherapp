from django.shortcuts import render, reverse, redirect
from django.conf import settings
from weatherapp.api import WeatherDataFetcher, build_redirect_url


def home(request):
    if request.method == "POST":
        query = request.POST.get("query", None)
        if query:
            return build_redirect_url(url="weatherapp:results", params={"query": query})
    return render(request, "index.html", {})


def results(request):
    query = request.GET.get("query", None)
    if query:
        results = WeatherDataFetcher(query=query).fetch_data()
        if results:
            context = {
                "results": results,
                "query": query,
            }

            return render(request, "results.html", context)

    return redirect(reverse("weatherapp:home"))
