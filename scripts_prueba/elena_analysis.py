# Import necessary libraries
import pandas as pd
import os
import time
import krakenex
import plotly.graph_objects as go
import streamlit as st
from pykrakenapi import KrakenAPI # Note: pykrakenapi requires Python >= 3.3, krakenex >= 2.0.0 and pandas

# Import modules and respective functions
from extract_data_module import *
from preprocessing_module import *

# ---MEDIA MOVL---

def get_periodos_user():
    """"""
    while True:
        try:
            periodos = int(input('¿Cuantos periodos anteriores te gustaría calcular la Media Movil?'))
            if periodos > 0:
                break
            else:
                print("Debe ser un numero entero mayor que cero")
        except ValueError:
            print('Invalid')
            continue
    return periodos

def get_media_movil(df, periodos):
    """Get the media movil
    :param df: pandas dataframe
    :param periodos: int value greater than cero (given by the user)
    :return: a pandas series"""
    return pd.Series(pd.Series.rolling(df['close'], periodos).mean())


# ---Relative Strength Index---

def get_rsi(df, periodosRSI = 14):
    """Function that calculates the RSI (Relative Strength Index)
    :param df: pandas dataframe
    :param periodosRSI: it refers to the 12 months of the year and a range, so 14 is a used value in practice
    :return: float value (rsi)"""
    valor_cerrado = df['close'].diff() # series pandas
    valor_cerrado.dropna(inplace=True)

    up = valor_cerrado.clip(lower=0) # series pandas
    df_up = pd.DataFrame(up)
    up_average = df_up.rolling(window=periodosRSI, min_periods=periodosRSI).mean()

    down = -1 * valor_cerrado.clip(upper=0) # series pandas
    df_down = pd.DataFrame(down)
    down_average = df_down.rolling(window=periodosRSI, min_periods=periodosRSI).mean()

    rs = up_average / down_average
    rsi = 100 - (100 / (1 + rs))

    return rsi


# --- Graphs ---
def get_grafico_cotizaciones(df, cripto):
    """"""
    grafico_coti = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df['open'],
                                             high=df['high'],
                                             low=df['low'],
                                             close=df['close'],
                                             ),
                              go.Scatter(x=df.index, y=df['close'], line=dict(color='pink', width=2))])
    titulo = 'Cotizacion de la criptomoneda: ' + cripto
    grafico_coti.update_layout(
        title=titulo,
        yaxis_title='Valor de cierre'
    )
    return grafico_coti

def get_grafico_media_movil(mm, cripto):
    """"""
    grafico_mm = go.Figure(data=[go.Scatter(x=mm.index, y=mm['close'], line=dict(color='blue', width=3))])
    titulo_mm = 'Media Móvil de la criptomoneda: ' + cripto
    grafico_mm.update_layout(
        title=titulo_mm,
        yaxis_title='Valor de cierre'
    )
    return grafico_mm

def get_grafico_rsi(rsi, cripto):
    """"""
    grafico_rsi = go.Figure(data=[go.Scatter(x=rsi.index, y=rsi['close'], line=dict(color='red', width=3))])
    titulo_rsi = 'RSI de la criptomoneda: ' + cripto
    grafico_rsi.update_layout(
        title=titulo_rsi,
        yaxis_title='Valor de cierre'
    )
    return grafico_rsi



def graficos_pro(df, mm, cripto):
    """"""
    st.title("Final Project Python for Data Analysis")
    st.markdown("Done by: Elena Martin de Diego and Patricia Kremer Deve")
    st.header("Datos de la criptomoneda " + cripto + " escogida")
    st.markdown("")
    st.dataframe(df.head())
    st.header("Cotizacion de la criptomoneda " + cripto)
    st.subheader("Cotizacion: Tasación oficial del valor de un título admitido a negociación en un mercado bursátil.")
    st.markdown("")
    st.plotly_chart(get_grafico_cotizaciones(df, cripto))
    st.header("Media Móvil de la moneda")
    st.subheader("Media Móvil: ")
    st.markdown("")
    st.plotly_chart(get_grafico_media_movil(mm, cripto))
    st.header("RSI de la moneda " + cripto)
    st.subheader("RSI: ")
    st.markdown("")
    st.plotly_chart(get_grafico_rsi(get_rsi(df, periodosRSI = 14), cripto))



def main_analysis():
    dir_path = 'data'
    data_name = 'dataset_to_process'
    #name_file = 'Possible_Currencies'

    #interval = 60  # mins, it will be used when downloading the data from the API, just to make sure the data extracted is from the last hour
    #api = krakenex.API()  # Instance of the krakenex.API class
    #k = KrakenAPI(api)  # Implements the Kraken API methods using the low-level krakenex python


    cripto = main_extract_data()
    print("La cripto es:", cripto)
    print('ok')
    main_preprocessing()
    print('ok')

    df = pd.read_csv('{}.csv'.format(os.path.join(dir_path, data_name)))

    media_movil = get_media_movil(df, get_periodos_user())

    get_rsi(df)

    graficos_pro(df, media_movil, cripto)

if __name__ == "__main__":

    dir_path = 'data'
    data_name = 'dataset_to_process'
    name_file = 'Possible_Currencies'

    interval = 60  # mins, it will be used when downloading the data from the API, just to make sure the data extracted is from the last hour

    api = krakenex.API()  # Instance of the krakenex.API class
    k = KrakenAPI(api)  # Implements the Kraken API methods using the low-level krakenex python
    info_df = k.get_asset_info  # Some information of the dataset extracted

    main_analysis()
