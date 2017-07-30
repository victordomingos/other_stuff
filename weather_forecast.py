#!/usr/bin/python3

import requests 
import sys
import json


# API provider: http://openweathermap.org/
APIKEY = '746310c71b33370d5655e5724893b037'
LOCATION = 'Braga,pt'
API_URL = 'http://api.openweathermap.org/data/2.5/forecast'


def get_weather_data():
    try:            
        params = {'q': LOCATION,
                  'APPID': APIKEY,
                  'units': 'metric',
                  'lang': 'pt',
                  'mode': 'json'}
                  
        json_data = requests.get(API_URL, params=params, timeout=(1,2)).json()
        return json_data
        
    except Exception as e:            
        print(e)
        sys.exit(1)
    

previsoes = get_weather_data()['list']

for previsao in previsoes:
    data = previsao['dt_txt'].replace(':00:00', 'h')
    temperatura_int = int(previsao['main']['temp'])
    temperatura = str(temperatura_int)+'ºC'
    tempo = previsao['weather'][0]['description']
    #pressao_int = int(previsao['main']['pressure'])
    #pressao = str(pressao_int)+'hPa'
    
    print(data, temperatura, tempo)