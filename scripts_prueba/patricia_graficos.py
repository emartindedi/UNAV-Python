
'''Hemos importado las librerias de pandas, matplotlib, virtualenvir...'''
import pandas as pd
import krakenex
from pykrakenapi import KrakenAPI
import plotly.graph_objects as go
import time
'''importamos esta porque nos salta los 5seg'''

'''Nos conectamos con la red'''
interval = 60
api = krakenex.API()
k = KrakenAPI(api)
data = k.get_asset_info

pairs = k.get_tradable_asset_pairs()
print(pairs)

'''Creamos el input que le llamamos moneda y moneda 2. Aquí nos dejará escojer que dos tipos de moneda queremos extraer los datos.'''
moneda = input('Introduce la criptomoneda que quieras')
moneda2 = input('Introduce la criptomoneda2')

'''Estamos poniendo las dos cotizaciones que el ususario quiere. Saldrá una tabla con todas las variables '''
valor, last1 = k.get_ohlc_data(moneda, interval=interval)
valor.sort_values(by='dtime',inplace=True)
print(valor)
valor2, last2 = k.get_ohlc_data(moneda2, interval=interval)
valor2.sort_values(by='dtime',inplace=True)
print(valor2)
time.sleep(5)








'''lo que estamos haciendo es graficar la criptomoneda1 que ha solicitado el usuario. Usamos el Candlestrick porque es un sistema efectivo para poder hacer el grafico de forma correcta.'''
grafico = go.Figure(data=[go.Candlestick(x=valor.index,
                                          open = valor['open'],
                                          high = valor['high'],
                                          low = valor['low'],
                                          close= valor['close'],
                                         ),
                          go.Scatter(x=valor.index, y=valor['close'], line=dict(color='pink', width=3))])
grafico.show()


'''Media movil cripto'''
periodos = int(input('¿Cuantos periodos anteriores te gustaría calcular la Media Movil?'))

def mediamovil(valor, periodos):
    mediamovil = pd.Series(pd.Series.rolling(valor['close'],periodos).mean())
    return valor
x=mediamovil(valor, periodos)
print(x)






grafico2 = go.Figure(data=[go.Scatter(x=x.index, y=x['close'], line=dict(color='blue', width=3))])
grafico2.update_layout(title='Media Movil')
grafico2.show()










'''RSI moneda'''

v_cerrado = valor['close'].diff()
v_cerrado.dropna(inplace=True)

periodosRSI = 14

up = v_cerrado.clip(lower=0)
updatafra = pd.DataFrame(up)
up_aver1= updatafra.rolling(window=periodosRSI, min_periods=periodosRSI).mean()


down = -1 * v_cerrado.clip(upper=0)
downdatafra= pd.DataFrame(down)
down_aver1= downdatafra.rolling(window=periodosRSI, min_periods=periodosRSI).mean()

rs = up_aver1 / down_aver1
rsi = 100 - (100 / (1 + rs))
print(rsi)








graficoRSI = go.Figure(data=[go.Scatter(x=rsi.index, y=rsi['close'], line=dict(color='red', width=3))])
graficoRSI.show()


