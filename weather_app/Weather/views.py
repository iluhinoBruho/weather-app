from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from collections import defaultdict

# Create your views here.

def index(request):
    appide = '82b797b6ebc625032318e16f1b42c016'
    #'b6907d289e10d714a6e88b30761fae22'
    #'82b797b6ebc625032318e16f1b42c016'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appide

    cities = City.objects.all()
    all_cities = []

    context = {'cur':[]}

    used = []
    used = defaultdict(bool)
    for ct in cities:
        current = ct.name
        if not used[current]:
            res = requests.get(url.format(ct.name)).json()
            city_info = {'city':ct.name, 'temp':res["main"]["temp"], 'icon':res["weather"][0]["icon"]}
            all_cities.append(city_info)
            used[current] = True

    context['all_info'] = all_cities

    if(request.method == 'POST'):
        now = request.POST
        form = CityForm(now)
        res = requests.get(url.format(now['name'])).json()
        if not used[now["name"]]:
            form.save()
            context['all_info'].append({'city':now["name"], 'temp':res["main"]["temp"], 'icon':res["weather"][0]["icon"]})

        out = {
        'city':now['name'],
        'temp':res["main"]["temp"],
        'icon':res["weather"][0]["icon"],
        'pressure':res["main"]["pressure"],
        'humidity':res["main"]["humidity"],
        'wind':res["wind"]["speed"],
        }
        try:
            out['visibility'] = res["visibility"]
        except:
            out['visibility'] = "no info"



        context['cur'] = [out]


    form = CityForm()
    context['form'] = form


    print(context)
    return render(request, 'Weather/index.html', context)
