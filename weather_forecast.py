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

from pprint import pprint


__app_name__ = "The NPK Weather App"
__author__ = "Victor Domingos"
__copyright__ = "© 2017 Victor Domingos"
__license__ = "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
__version__ = "0.9"
__email__ = "info@victordomingos.com"
__status__ = "beta"


# ---------- Set these variables before use ----------
# Request an API key at: http://openweathermap.org/
APIKEY = 'APIKEY'
API_URL_CURRENT = 'http://api.openweathermap.org/data/2.5/weather'
API_URL = 'http://api.openweathermap.org/data/2.5/forecast'

LOCATION = 'Braga,pt'

HEADER_FONTSIZE = 16
TITLE_FONTSIZE = 12
TABLE_FONTSIZE = 10.5

# Set to True to see more data (forecast for each 3h)
DETAILED = False

# Set accordingly with Pythonista app current settings
DARK_MODE = False
# ----------------------------------------------------


def dayNameFromWeekday(weekday):
    days = ["Segunda-feira", "Terça-feira", "Quarta-feira",
            "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    return days[weekday] if -1 < weekday < len(days) else None


def converter_vento(graus, metros_p_segundo):
    direcoes = ["N","NE","E","SE","S","SO","O","NO","N"]
    posicao = int((graus+57.5)/45)-1
    kmph = int(metros_p_segundo*3.6)
    return (direcoes[posicao], kmph)


def obter_nuvens(json):
    nuvens_str = ''
    if 'clouds' in json.keys():
        nuvens = json['clouds']['all']
        if nuvens == 0:
            return ''
        nuvens_str = 'N.'+str(nuvens)+'%'
    return nuvens_str
    
    
def obter_humidade(json):
    humidade_str = ''
    if 'humidity' in json['main'].keys():
        humidade = json['main']['humidity']
        if humidade == 0:
            return ''
        humidade_str = 'H.'+str(humidade)+'%'
    return humidade_str

        
def formatar_tempo(tempo,icone,chuva,ahora):
    if tempo == 'Céu Claro':
        tempo = 'Céu Limpo'
        if ahora in ['22h', '01h', '04h']:
            icone = '🌙'
        else:
            icone = '☀️'
    elif tempo == 'Nuvens Quebrados':
        tempo = 'Céu Muito Nublado'
        icone = '☁️'
    elif tempo in ('Algumas Nuvens', 'Nuvens Dispersas'):
        tempo = 'Céu Pouco Nublado'
        icone = '⛅️'
    elif ('Nublado' in tempo):
        icone = '☁️'
    elif ('Neblina' in tempo):
        icone = '🌤'
        
    if 'Chuva' in tempo:
        tempo = tempo + ' ' + chuva

    return (tempo, icone)
    

def get_weather_data(kind='forecast'):
    if kind == 'forecast':
        api_URL = API_URL
    else:
        api_URL = API_URL_CURRENT
        
    try:            
        params = {'q': LOCATION,
                  'APPID': APIKEY,
                  'units': 'metric',
                  'lang': 'pt',
                  'mode': 'json'}
                  
        json_data = requests.get(api_URL, params=params, timeout=(1,2)).json()
        return json_data
        
    except Exception as e:            
        print(e)
        sys.exit(1)


def mostra_previsao():
    previsoes = get_weather_data(kind='forecast')['list']
    agora = arrow.now().time().hour
    data_anterior = ''
    
    for previsao in previsoes:             
        icone = ''       
        data = previsao['dt_txt'].split()[0]
        
        adata = arrow.get(previsao['dt']).to('local')
        ahora = adata.to('local').format('HH')+'h'
         
        hoje = arrow.now().date().day
        amanha = hoje + 1
        adata_dia = adata.date().day
        adata_hora = adata.time().hour
        if adata_dia == amanha:
            adata_hora += 24
        
        if (hoje == adata_dia) or ((amanha == adata_dia) and agora <= adata_hora):
            show_more_info = True
            #print('show_more_info true')
        else:
            show_more_info = False
            #print('show_more_info false')    
        
        if (not DETAILED) and (not show_more_info):
            if ahora in ('04h','07h','22h','01h'):
                if ahora is '01h':
                    data_anterior = data
                #print('continue')
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
                tempo, chuva, icone = formatar_chuva(tempo,previsao['rain']['3h'])
            else:
                chuva = ''
        else:
            chuva = ''
            
        nuvens_str = obter_nuvens(previsao)
        humidade = obter_humidade(previsao)
        
        line_size = 45
        str_dia = ''
        spaces = ''
        console.set_font("Menlo-Bold", TITLE_FONTSIZE)
        if data_anterior == '':
            if hoje == adata_dia:
                str_dia = 'Hoje (' + data_curta + ')'
                spaces = '_'*(line_size-len(str_dia))
                str_dia = str_dia + spaces
                print('\n'+str_dia)
            else:
                print('\nAmanhã ('+data_curta+')')
        elif data == data_anterior:
            pass
        else:
            dia_da_semana = dayNameFromWeekday(arr_data.weekday())
            print('\n'+dia_da_semana+' ('+data_curta+')')
        
    
        console.set_font("Menlo-Regular", TABLE_FONTSIZE)
        tempo, icone = formatar_tempo(tempo,icone,chuva,ahora)
        
        print(' ', ahora, temperatura, icone, tempo, nuvens_str)
        data_anterior = data
        
        
def mostra_estado_atual():
    estado = get_weather_data(kind='current')
    adata = arrow.get(estado['dt']).to('local')
    ahora = adata.to('local').format('HH')+'h'
    temperatura_int = int(estado['main']['temp'])
    temperatura = str(temperatura_int)+'°'
    tempo = estado['weather'][0]['description'].title()
    pressao = str(estado['main']['pressure'])+'hPa'
    vento_dir = estado['wind']['deg']
    vento_veloc = estado['wind']['speed']
    nuvens = estado['clouds']['all']
    str_tempo, icone = formatar_tempo(tempo,'','',ahora)
        
    if 'rain' in estado.keys():
        if '3h' in estado['rain'].keys():
            tempo, chuva, icone = formatar_chuva(tempo,estado['rain']['3h'])
        else:
            chuva = ''
    else:
        chuva = ''
        
    nuvens_str = obter_nuvens(estado)
    humidade = obter_humidade(estado)
    
    adata_nascer = arrow.get(estado['sys']['sunrise']).to('local')
    ahora_nascer = adata_nascer.to('local').format('HH:mm')
    
    adata_por = arrow.get(estado['sys']['sunset']).to('local')
    ahora_por = adata_por.to('local').format('HH:mm')
    
    direcao, velocidade = converter_vento(vento_dir, vento_veloc)
    
    str_humidade = ' Humidade: ' + humidade
    str_pressao = ' Pressão: ' + pressao
    str_vento = ' Vento: ' + direcao + ' ' + str(velocidade)+'km/h'
    
    str_nascer = 'Nascer do sol: ' + ahora_nascer
    str_por = 'Pôr do sol: ' + ahora_por
    
    
    line_size = 52
    line1_spaces = ' '*(line_size-len(str_humidade)-len(str_nascer))
    line2_spaces = ' '*(line_size-len(str_pressao)-len(str_por))
    
    console.set_font("Menlo-Bold", TITLE_FONTSIZE)
    print('\nAgora mesmo:', icone, temperatura)
    console.set_font("Menlo-Regular", TABLE_FONTSIZE)
    print(' ', str_tempo, nuvens_str, chuva)
    print('  Vento:', direcao, str(velocidade)+'km/h')
    
    str1 = ' {}{}{}'.format(str_humidade,line1_spaces, str_nascer)
    str2 = ' {}{}{}'.format(str_pressao,line2_spaces, str_por)
    print(str1)
    print(str2)
    
    
    #print('  Humidade:', humidade)
    
    
    #print('  Pressão:', pressao)
    
    
    #print('  Nascer do sol:', ahora_nascer)
    #print('  Pôr do sol:', ahora_por)
    



def formatar_chuva(tempo, que_chuva):
    chuva = str(que_chuva)
    fchuva = float(chuva)
    
    chuva = '({}mm/h)'.format(str(round(fchuva/3,1)))
    icone = '🌧'
    
    if fchuva < .75:
        if tempo == 'Chuva Fraca':
            tempo = 'Possib. Chuva Fraca'
        icone = '☁️'
    elif .75 <= fchuva < 3:
        chuva += '💧'
    elif 3 <= fchuva < 12:
        chuva += '💧💧'
    elif 12 <= fchuva < 48:
        chuva += '💧💧💧'
    elif 48 <= fchuva:
        chuva += '💦💦☔️💦💦'
    return (tempo, chuva, icone)




def config_consola():
    '''
    Sets console font size and color for Pythonista on iOS
    '''
    console.clear()
    console.set_color(.5,.5,.5)
    console.set_font("Menlo-Bold",HEADER_FONTSIZE)
    
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
    mostra_estado_atual()
    mostra_previsao()
    