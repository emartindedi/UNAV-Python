# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dataclasses import dataclass
"""Module to analyze and graphic the data"""

@dataclass()
class Analyze:

    colors_plots = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    def __init__(self, df, cripto):
        self.df = df
        self.cripto = cripto

    def __post_init__(self):
        self.media_movil = None
        self.rsi: float = 0


    def get_periodos_user(self):
        """Extract the periods given by the user
        :return: integer"""
        while True:
            try:
                periodos = int(input('¿Cuantos periodos anteriores te gustaría calcular la Media Movil?'))
                if (periodos > 0 and periodos <= 200):
                    break
                else:
                    print("Debe ser un numero entero mayor que cero y menor que doscientos dias")
            except ValueError:
                print('Invalid')
                continue
        return periodos

    def get_media_movil(self, periodos):
        """Get the media movil
        :param df: pandas dataframe
        :param periodos: int value greater than cero and less than 200 (given by the user)
        :return: a pandas series"""
        return pd.Series(pd.Series.rolling(self.df['close'], periodos).mean())

    def get_rsi(self, periodosRSI=14):
        """Function that calculates the RSI (Relative Strength Index)
        :param df: pandas dataframe
        :param periodosRSI: it refers to the 12 months of the year and a range, so 14 is a used value in practice
        :return: float value (rsi)"""
        valor_cerrado = self.df['close'].diff()  # series pandas
        valor_cerrado.dropna(inplace=True)

        up = valor_cerrado.clip(lower=0)  # series pandas
        df_up = pd.DataFrame(up)
        up_average = df_up.rolling(window=periodosRSI, min_periods=periodosRSI).mean()

        down = -1 * valor_cerrado.clip(upper=0)  # series pandas
        df_down = pd.DataFrame(down)
        down_average = df_down.rolling(window=periodosRSI, min_periods=periodosRSI).mean()

        rs = up_average / down_average
        rsi = 100 - (100 / (1 + rs))
        print(rsi.head())
        return rsi

    def economy(self):
        """Save the values in the class"""
        self.media_movil = self.get_media_movil(self.get_periodos_user())
        self.rsi = self.get_rsi()


    def get_grafico_cotizaciones(self):
        """Get the graphic of the cotizacion"""
        grafico_coti = go.Figure(data=[go.Candlestick(x=self.df.index,
                                                      open=self.df['open'],
                                                      high=self.df['high'],
                                                      low=self.df['low'],
                                                      close=self.df['close'])])
        titulo = 'Cotizacion de la criptomoneda: ' + self.cripto
        grafico_coti.update_layout(
            title=titulo,
            yaxis_title='Valor de cierre',
            xaxis_title='Mes-Dia'
        )
        return grafico_coti

    def get_grafico_media_movil(self):
        """Graphic of the media movil"""
        grafico_mm = go.Figure(data=[go.Scatter(x=self.df.index, y=self.df['close'], line=dict(color=self.colors_plots[0], width=3))])
        titulo_mm = 'Media Móvil de la criptomoneda: ' + self.cripto
        grafico_mm.update_layout(
            title=titulo_mm,
            yaxis_title='Valor de cierre',
            xaxis_title='Mes-Dia'
        )
        return grafico_mm

    def get_grafico_rsi(self, rsi):
        """Graphic of rsi"""
        grafico_rsi = go.Figure(data=[go.Scatter(x=rsi.index, y=rsi['close'], line=dict(color=self.colors_plots[1], width=1.5))])
        titulo_rsi = 'RSI de la criptomoneda: ' + self.cripto
        grafico_rsi.update_layout(
            title=titulo_rsi,
            yaxis_title='Valor de cierre',
            xaxis_title='Mes-Dia'
        )
        return grafico_rsi

    def get_grafico_cotizacion_media_movil(self):
        grafico_coti_mm = go.Figure(data=[go.Candlestick(x=self.df.index,
                                                      open=self.df['open'],
                                                      high=self.df['high'],
                                                      low=self.df['low'],
                                                      close=self.df['close']),
                        go.Scatter(x=self.df.index, y=self.df['close'], line=dict(color=self.colors_plots[3], width=0.8))])
        titulo = 'Cotizacion junto con la media movil de la criptomoneda: ' + self.cripto
        grafico_coti_mm.update_layout(
            title=titulo,
            yaxis_title='Valor de cierre',
            xaxis_title='Mes-Dia'
        )
        return grafico_coti_mm


    def graficos_pro(self):
        """Streamlit"""
        st.title("Final Project Python for Data Analysis")
        st.markdown("Done by: Elena Martin de Diego and Patricia Kremer Devesa")
        st.header("Datos de la criptomoneda " + self.cripto + " escogida")
        st.markdown("")
        st.dataframe(self.df.head())

        st.header("Cotizacion de la criptomoneda " + self.cripto)
        st.subheader(
            "Cotizacion: Tasación oficial del valor de un título admitido a negociación en un mercado bursátil.")
        st.markdown("")
        st.plotly_chart(self.get_grafico_cotizaciones())

        st.header("Media Móvil de la moneda")
        st.markdown("La media móvil es un indicador técnico que calcula media de los precios en un periodo de tiempo establecido. Con ello se divide entre el numero total de datos recogido y se obtiene la línea de tendencia.")
        st.plotly_chart(self.get_grafico_media_movil())

        st.header("RSI de la moneda " + self.cripto)
        st.markdown("El RSI también denomiando Relative Strength Index es una herramienta económica para observar si los activos que se evalúan han presentado una tendencia de sobrecompra o sobreventa.")
        st.plotly_chart(self.get_grafico_rsi(self.get_rsi(periodosRSI=14)))

        st.header("Gráfico conjunto de la cotizacion y la media móvil de la moneda", self.cripto)
        st.markdown("")
        st.plotly_chart(self.get_grafico_cotizacion_media_movil())