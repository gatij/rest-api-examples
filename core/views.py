from django.shortcuts import render
from django.conf import settings

import requests
from github import Github, GithubException
from .forms import DictionaryForm

def weather(request):
    url = 'https://api.airvisual.com/v2/nearest_city'
    urlD = 'https://api.airvisual.com/v2/city'
    payload = {'key':settings.AIR_API_KEY}
    response = requests.get(url,params = payload).json()
    cities = ["New Delhi","Mumbai","Kolkata","Chennai","Ghandinagar"]
    states = ['Delhi','Maharashtra','West Bengal','Tamil Nadu','Gujarat']
    AQI = []
    for city,state in zip(cities,states):
        headers={}
        headers['city']=city
        headers['state']=state
        headers['country']='India'
        headers['key']= settings.AIR_API_KEY
        responseD = requests.get(urlD,params = headers).json()
        aqi_city = responseD['data']['current']['pollution']['aqius']
        AQI.append(aqi_city)
    
    aqi = response['data']['current']['pollution']['aqius']
    AQI.append(aqi)   
    cities.append(response['data']['city'])
    return render(request, 'core/weather.html',{'cities':cities,'AQI':AQI} )

def home(request):
    search_result = {}
    sun_result = {}
    params = {'access_key': settings.IPSTACK_API_KEY}
    #print(search_result['map_api_key'])
    if 'ipaddress' in request.GET:
        ip_address = request.GET['ipaddress']
        #print(search_result['map_api_key'])
        response = requests.get('http://api.ipstack.com/%s' % ip_address, params=params)
        #print(response.url)
        search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
        search_result = response.json()
        search_result['map_api_key'] = settings.GOOGLE_MAPS_API_KEY
        search_result['success'] = search_was_successful
        sun_response = requests.get("https://api.sunrise-sunset.org/json?lat=%s&lng=-%s&date=today" % (search_result['longitude'],search_result['latitude']) )
        #print(sun_response.url)
        sun_result = sun_response.json()
        #print(search_result)
        #print(search_result['country_code'])
        #search_result['flag_url']="<img src=" + search_result['country_flag'] + " alt='Smiley face' height='42' width='42'> "

    return render(request, 'core/home.html', {'search_result': search_result,'sun_result': sun_result})

def github(request):
    search_result = {}
    if 'username' in request.GET:
        username = request.GET['username']
        url = 'https://api.github.com/users/%s' % username
        response = requests.get(url)
        search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
        search_result = response.json()
        search_result['success'] = search_was_successful
        search_result['rate'] = {
            'limit': response.headers['X-RateLimit-Limit'],
            'remaining': response.headers['X-RateLimit-Remaining'],
        }
    return render(request, 'core/github.html', {'search_result': search_result})


def github_client(request):
    search_result = {}
    if 'username' in request.GET:
        username = request.GET['username']
        client = Github()

        try:
            user = client.get_user(username)
            search_result['name'] = user.name
            search_result['login'] = user.login
            search_result['public_repos'] = user.public_repos
            search_result['success'] = True
        except GithubException as ge:
            search_result['message'] = ge.data['message']
            search_result['success'] = False

        rate_limit = client.get_rate_limit()
        search_result['rate'] = {
            'limit': rate_limit.rate.limit,
            'remaining': rate_limit.rate.remaining,
        }

    return render(request, 'core/github.html', {'search_result': search_result})


def oxford(request):
    search_result = {}
    if 'word' in request.GET:
        form = DictionaryForm(request.GET)
        if form.is_valid():
            search_result = form.search()
    else:
        form = DictionaryForm()
    return render(request, 'core/oxford.html', {'form': form, 'search_result': search_result})
