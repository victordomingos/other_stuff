import requests 
import sys
import json
import arrow
from pprint import pprint


# API provider: please check http://openweathermap.org/
APIKEY = 'APIKEY'
API_URL = 'http://api.openweathermap.org/data/2.5/forecast'

# Enter your location here (City, contry code)
LOCATION = 'Esposende,pt'


def dayNameFromWeekday(weekday):
    days = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    return days[weekday] if 0 < weekday < len(days) else None

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


data_anterior = ''
for previsao in previsoes:
    icone = ''
    data, hora = previsao['dt_txt'].replace(':00:00', 'h').split()
    temperatura_int = int(previsao['main']['temp'])
    temperatura = str(temperatura_int)+'ºC'
    tempo = previsao['weather'][0]['description'].title()
    #pressao_int = int(previsao['main']['pressure'])
    #pressao = str(pressao_int)+'hPa'
    arr_data = arrow.get(data)
    data_curta = arr_data.format('DD/MM')
    
    if 'rain' in previsao.keys():
        if '3h' in previsao['rain'].keys():
            chuva = str(previsao['rain']['3h'])
            icone = '🌧'
            fchuva = float(chuva)
            if fchuva < .75:
                chuva = '❔'
            elif .75 <= fchuva < 1.5:
                chuva = '💧'
            elif 1.5 <= fchuva < 1.5:
                chuva = '💧💧'
            elif 1.5 <= fchuva < 3:
                chuva = '💧💧💧'
            elif 1.5 <= fchuva < 3:
                chuva = '💦💦☔️💦💦'
            
        else:
            chuva = ''
    else:
        chuva = ''
    
    if data_anterior == '':
        print('\nHoje ('+data_curta+')')
    elif data == data_anterior:
        pass
    else:
        dia_da_semana = dayNameFromWeekday(arr_data.weekday())
        print('\n'+dia_da_semana+' ('+data_curta+')')


    if tempo == 'Céu Claro':
        tempo = 'Céu Limpo'
        icone = '☀️'
    elif tempo == 'Nuvens Quebrados':
        tempo = 'Céu Muito Nublado'
        icone = '☁️'


    if ('Nuvens' in tempo):
        icone = '☁️'
    if 'Chuva' in tempo:
        tempo = tempo + ' ' + chuva
    
    
    print(' ', hora, temperatura, icone, tempo)
    data_anterior = data