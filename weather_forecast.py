'''
A little utility to check the weather forecast for the next few days. This 
version is custom made for iPhone, so it uses Pythonista 3. It makes use of 
the web API provided by openweathermap.org and requires 'arrow' (which you can
install with pip using StaSh).

Developed in Python 3.5 for your enjoyment by:
        Victor Domingos
        http://victordomingos.com

© 2017 Victor Domingos
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
'''

import requests 
import sys
import json
import arrow
import console


__app_name__ = "The NPK Weather App"
__author__ = "Victor Domingos"
__copyright__ = "Copyright 2017 Victor Domingos"
__license__ = "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
__version__ = "0.9"
__email__ = "info@victordomingos.com"
__status__ = "beta"


# ---------- Set these variables before use ----------
# Request an API key at: http://openweathermap.org/
APIKEY = 'APIKEY'
API_URL = 'http://api.openweathermap.org/data/2.5/forecast'

LOCATION = 'Braga,pt'

TITLE_FONTSIZE = 16
TABLE_FONTSIZE = 11

# Set to True to see more data (forecast for each 3h)
DETAILED = False

# Set accordingly with Pythonista app current settings
DARK_MODE = False
# ----------------------------------------------------


def dayNameFromWeekday(weekday):
    days = ["Segunda-feira", "Terça-feira", "Quarta-feira",
            "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    return days[weekday] if -1 < weekday < len(days) else None


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


def mostra_previsao():
    previsoes = get_weather_data()['list']

    data_anterior = ''
    for previsao in previsoes:             
        icone = ''       
        data = previsao['dt_txt'].split()[0]
        
        adate = arrow.get(previsao['dt'])
        ahora = adate.to('local').format('HH')+'h'
        
        if not DETAILED and data_anterior != '':
            if ahora in ('01h','04h','07h','22h'):
                continue
        
        temperatura_int = int(previsao['main']['temp'])
        temperatura = str(temperatura_int)+'°'
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
        
        
        console.set_font("Menlo-Bold", TABLE_FONTSIZE)
        if data_anterior == '':
            print('\nHoje ('+data_curta+')')
        elif data == data_anterior:
            pass
        else:
            dia_da_semana = dayNameFromWeekday(arr_data.weekday())
            print('\n'+dia_da_semana+' ('+data_curta+')')
    
        console.set_font("Menlo-Regular", TABLE_FONTSIZE)
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
        
        print('  ', ahora, temperatura, icone, tempo)
        data_anterior = data
        
    
def config_consola():
    '''
    Sets console font size and color for Pythonista on iOS
    '''
    console.clear()
    console.set_color(.5,.5,.5)
    console.set_font("Menlo-Bold",TITLE_FONTSIZE)
    
    if DARK_MODE:
        console.set_color(0.5, 0.8, 1)
    else:
        console.set_color(0.2, 0.5, 1)
        
    print("{0} ({1})".format(__app_name__, LOCATION))
    console.set_font("Menlo-Regular", 6.7)
    
    if DARK_MODE:
        console.set_color(0.7, 0.7, 0.7)
    else:
        console.set_color(0.5, 0.5, 0.5)
    print('{}, {}'.format(__copyright__, __license__))
    
    console.set_font("Menlo-Regular", TABLE_FONTSIZE)
    
    if DARK_MODE:
        console.set_color(1, 1, 1)
    else:
        console.set_color(0,0,0)
        

if __name__ == "__main__":
    config_consola()
    mostra_previsao()