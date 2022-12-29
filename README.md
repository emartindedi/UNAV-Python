# Final Project: Python para el Analisis de Datos

---

**Master Oficial of Big Data Science** @ University of Navarra.

---


El proyecto consistirá en ser capaces de bajar la cotización de un par de monedas, un ejemplo de cotizaciones en Kraken:
https://www.kraken.com/es-es/prices?quote=EUR

Después de bajarlas, será necesario hacer una gráfica del movimiento que ha tenido.

Además, se hará una gráfica de la media móvil:
https://www.rankia.com/diccionario/trading/medias-moviles

Para descargarlo localmente:

```python
$ git clone https://github.com/emartindedi/UNAV-Python.git
```


## Índice  <a name="indice"></a>

- [Objetivos](#obj)
- [Extract the data](#extract_data)
  - [save\_currencies](#save_currencies)
  - [ask\_user\_for\_currency](#ask_user_for_currency)
  - [user\_select\_currency](#user_select_currency)
  - [get\_dataframe\_to\_process](#get_dataframe_to_process)
- [Process the data](#preprocessing)
  - [explore_dataset](#explore_dataset)
  - [missing_values](#missing_values)
  - [get_percentile](#get_percentile)
  - [delete_outliers](#delete_outliers)
  - [clean_columns](#clean_columns)
  - [clean_rows](#clean_rows)
  - [general_clean](#general_clean)
- [Analyze the data and visualizations](#Analyze)
  - [get_periodos_user](#get_periodos_user)
  - [get_media_movil](#get_media_movil)
  - [get_rsi](#get_rsi)
  - [economy](#economy)
  - [get_grafico_cotizaciones](#get_grafico_cotizaciones)
  - [get_grafico_media_movil](#get_grafico_media_movil)
  - [get_grafico_rsi](#get_grafico_rsi)
  - [get_grafico_cotizacion_media_movil](#get_grafico_cotizacion_media_movil)
  - [graficos_pro](#graficos_pro)
- [Workflow](#workflow) 
- [Conclusions](#conclusions)


---

# Objective <a name="obj"></a> 
[Volver al índice](#indice)

The main objective is to download the price of a specific currency, selected by the user, and graphic the movements. 
To understand better the changes it will be displayed some economic measures.

In order to achieve the goal, the project is divided into four files: extract_data.py, preprocessing.py, analysis.py and workflow.py.
The division of the code in classes and different files will help doing the project more modular and general.

To run the code, write in the terminal:

```python
$ cd .\scripts\
$ streamlit run .\workflow.py
```

Previously make sure that the specifications `requirements.txt` are the same as 
in the virtual enviroment that it's gonna be used to execute it.

---



# Extract the data<a name="extract_data"></a> 
[Volver al índice](#indice)

The extraction of the data will be performed using the package `krakenex` and specifically the library `pykrakenapi`. 
For more information about it visit https://github.com/dominiktraxl/pykrakenapi.

Before execute the code, it needs to be installed:
```
# install from PyPI
$ pip install krakenex
$ pip install pykrakenapi
```


Notice that the code related to the creation of the dataset is in the python file extract_data.py.

The class `Get_Data` has a unique attribute named `cripto_user_selected` which is initialized after, when the 
currency is written in the terminal.

```python
@dataclass()
class Get_Data:
    def __post_init__(self):
        self.cripto_user_selected = ''
```

This class has four different methods:
* save_currencies: save in a csv file all the possible currencies at the moment
* ask_user_for_currency: initialized the attribute cripto_user_selected with the selection made in the terminal
* user_select_currency: returns the dataset of the currency selected before
* get_dataframe_to_process:  **core** one which manages all the class and call the rest of the methods.

## save_currencies <a name="save_currencies"></a> 
[Volver al índice](#indice)

The method takes as inputs a directory path and the name of the csv file that will be created 
and saved it with all the possibles currencies at the moment in two columns.

First of all it's created an instance of the class KrakenAPI with input api to be able to connect to the 
API and extract the data.
Then if the folder does not exists, it's created inside the path where its executing. 
The possible currencies can be extracted in two formats (ex. EUR/USD and EURUSD), the format 'wsname' and 'altname' 
respectively. This information will be saved first in a dictionary and then in a pandas dataframe object
with the index the 'wsname' column.

```python
def save_currencies(self, dir_path, name_file):
    """save into a csv file the wsname and altname of the currencies availables in the kraken API
    : dir_path: path of the folder (directory) where it will be saved
    : name_file: name (without .csv) of the file where it will be saved"""
    api = krakenex.API()  # Instance of the krakenex.API class
    k = KrakenAPI(api)
    try:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)  # If it does not exist the directory, we create it
        currencies = dict(zip(k.get_tradable_asset_pairs()['wsname'],
                              k.get_tradable_asset_pairs()['altname']))  # Get the names of the currencies available
        df = pd.DataFrame.from_dict(currencies, orient='index',
                                    columns=['altname'])  # Transform the dictionary into a dataframe
        df.to_csv('{}.csv'.format(os.path.join(dir_path, name_file)))  # Save it
        print(f'Saved correctly:' '{}.csv'.format(os.path.join(dir_path, name_file)))
    except TypeError:
        print("The name of the file or the directory are incorrect")
```

## ask_user_for_currency <a name="ask_user_for_currency"></a> 
[Volver al índice](#indice)

This function, given the dataframe previously created with the currencies available, 
shows in the terminal the possible ones and takes the string written. It checks if the 
response to the question "Enter the abbreviation of the criptocurrency wanted:" makes sense, this is, 
if the answer is one of the 'wsname' obtained previously (index in the dataframe).
Finally, it saves the result in the attribute to use it later.

```python
def ask_user_for_currency(self, df):
    """ask the user a currency
    : df: pandas dataframe object which contains the wsname and altname of all the currencies availables in the kraken API
    : return: a string which contains the wsname of the currency selected by the user"""
    print("The possible answers are:")
    for idx, element in enumerate(list(df.index)):
        print("{}) {}".format(idx + 1, element))
    # print("The possible answers", df.index) more simple
    while True:
        try:
            user_curr = str(input("Enter the abbreviation of the criptocurrency wanted:"))
            if user_curr in df.index:
                break
            else:
                print("The currency is not available or it not correct")
        except ValueError:
            print('Invalid')
            continue
    self.cripto_user_selected = df.loc[user_curr]['altname']
    return user_curr
```

## user_select_currency <a name="user_select_currency"></a> 
[Volver al índice](#indice)

Now that is given as input the currency selected, it will be downloaded the
dataframe with the funcion 'get_ohlc_data', obtaining the data of the 60 min (interval) previously.

```python
def user_select_currency(self, curr):
    """get the data available for the currency which has wsname curr
    : df: pandas dataframe object which contains the wsname and altname of all the currencies availables in the kraken API
    : curr: a string which contains the wsname of the currency selected by the user
    : return: a tuple object which contains the dataframe for the currency curr and the last time"""
    interval = 60
    api = krakenex.API()  # Instance of the krakenex.API class
    k = KrakenAPI(api)
    k.get_tradable_asset_pairs()
    time.sleep(5)
    return (k.get_ohlc_data(curr, ascending=True, interval=interval))
```

## get_dataframe_to_process <a name="get_dataframe_to_process"></a> 
[Volver al índice](#indice)

This is the method to manage and execute the extraction of the data.
First, it's obtained the currencies available and read them (currencies_names_df). Then
it's saved in the attribute the currency selected by the user and printed.
After it, it's saved the data into a csv file ready to process.

```python
def get_dataframe_to_process(self, dir_path, name_file, data_name):
    """Manage the extraction of the dataset
    :param: dir_path: path of the folder (directory) where it will be saved
    :param: name_file: name (without .csv) of the file where it will be saved the currencies available
    :param: data_name: name (without .csv) of the file where it will be saved the dataframe"""
    # Obtain a csv file with all names of available currencies
    self.save_currencies(dir_path, name_file)

    # Save the currencies in a pandas dataframe
    currencies_names_df = pd.read_csv('{}.csv'.format(os.path.join(dir_path, name_file)), index_col=[0])

    # Ask the user for the currency wanted to analyze
    self.cripto_user_selected = currencies_names_df.loc[self.ask_user_for_currency(currencies_names_df)]['altname']

    print('You have selected: ', self.cripto_user_selected)

    try:

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)  # If it does not exist the directory, we create it

        data = self.user_select_currency(self.cripto_user_selected)[0]

        data.to_csv('{}.csv'.format(os.path.join(dir_path, data_name)))  # Save it
        print(f'Saved correctly: ' '{}.csv'.format(os.path.join(dir_path, data_name)))

    except OSError:
        print("The name of the file or the directory are incorrect")

    return self.user_select_currency(self.cripto_user_selected)
```

# Process the data <a name="preprocessing"></a> 
[Volver al índice](#indice)

The class `Preprocessing` in the file `preprocessing.py` will be the one used to process the dataset obtained in 
previous steps.

The class does not have any atrribute but has seven different methods:
* explore_dataset: exploratory analysis of the dataframe
* missing_values: function to treat the missing values
* get_percentile: useful to obtain the percentile 25,75, or any of a pandas series object.
* delete_outliers: used to delete the outliers of a column (pandas series)
* clean_columns: function that manages all the cleaning in columns
* clean_rows: function that manages all the cleaning in rows, this is, the duplicated samples
* general_clean: core method to process the data


## explore_dataset <a name="explore_dataset"></a> 
[Volver al índice](#indice)

Give a overview of the dataset given.

```python
def explore_dataset(self, df):
    """Function that print some information about the dataset
    :param df: pandas dataframe"""
    # The names of the columns are:
    print("The columns are:", df.columns)
    print("There are ", df.shape[1], " columns on the dataset and ", df.shape[0], "samples")
    print("", df.nunique())
    print(df.isna().any())
    print(type(df.isna().any()))
    # Descriptive Statistics
    stats = df.describe(include='all', datetime_is_numeric=True)
    print(stats)
```

## missing_values <a name="missing_values"></a> 
[Volver al índice](#indice)

This function ask the user what method to use to solve the issue of missing values. The 
possibilies are: deletion, mean or median.
After knowing the option selected it proceed acoording to it.

```python
def missing_values(self, df):
    """Function that given a dataset it creates a list with the columns that have some missing values. Then if there is not empty, the user
        is asked for the method to use
    :param df: pandas dataframe
    :return: the cleaned dataset with the method selected by the user: delete, mean or median are the options"""
    list_columns_missing = list()
    for col in df.columns:
        n_miss = df[col].isnull().sum()  # count number of rows with missing values
        if n_miss > 0:
            list_columns_missing.append(col)
    if len(list_columns_missing) != 0:
        print("The columns with missing values are:", list_columns_missing)
        while True:
            try:
                method_missing = str(input("Choose a method for the missing values: delete, mean, median"))
                if method_missing in ['delete', 'mean', 'median']:
                    break
                else:
                    print("Try again")

            except ValueError:
                print('Invalid')
                continue
        print("Proceed with the method", method_missing)
        if method_missing == 'delete':
            # drop rows with missing values
            df.dropna(inplace=True)
            # summarize the shape of the data with missing rows removed
            print("The shape after the removal of missing values is: ", df.shape)
        elif method_missing == 'mean':
            for col in list_columns_missing:
                df[col] = df[col].fillna(df[col].mean())
        else:
            if method_missing == 'median':
                for col in list_columns_missing:
                    df[col] = df[col].fillna(df[col].median())
    else:
        print("There are no missing values")
    return df
```

## get_percentile <a name="get_percentile"></a> 
[Volver al índice](#indice)

This method is used to know the percentile (percentile_rank) of a pandas series, the 
column (column) of the pandas dataframe df. It returns the integer of the index where is the
percentile_rank position.

```python
def get_percentile(self, df, percentile_rank, column):
    """Given a dataset and the column to calculate the percentile 75 and 25, it calculates the index position
    :param df : pandas dataframe
    :param percentile_rank: generally 75 or 25, a value between 0 and 100
    :param column: valid name column of the dataframe df
    :return: the element in the index and column passed"""

    # First, sort by ascending columns, reset the indices
    df = df.sort_values(by=column).reset_index()
    index = (len(df.index) - 1) * percentile_rank / 100.0
    index = int(index)
    return df.at[index, column]
```

## delete_outliers <a name="delete_outliers"></a> 
[Volver al índice](#indice)

The outliers can be treated or no and this decision is taken in the terminal. 
First its calculated the interquartile range in order to obtain the minimun and 
maximum non outlier value. Returns the non outlier values.

```python
def delete_outliers(self, df, column, k=1.5):
    """Given a dataset and the name of a column it calculates the outlier cutoff and identify the outliers
    :param df: pandas dataframe
    :param column: valid name column of the dataframe df
    :param k: contant (int) generally 1.5
    :return: the cleaned dataframe without outliers"""
    # Compute the 25th percentile, the 75th percentile and the IQR
    p25 = self.get_percentile(df, 25, column)
    p75 = self.get_percentile(df, 75, column)
    # calculate interquartile range
    iqr = p75 - p25

    # calculate the outlier cutoff
    # "Minimum non-outlier value": 25th percentile - 1.5 * IQR
    min_val = p25 - k * iqr
    # "Maximum non-outlier value": 75th percentile + 1.5 * IQR
    max_val = p75 + k * iqr
    print(f"The outlier cutoff is {min_val, max_val}")
    # print(f"The outlier cutoff is {min_val, max_val}", min_val, max_val)

    # identify outliers
    outliers = df[(df[column] < min_val) | (df[column] > max_val)]
    print('Identified outliers: %d' % outliers.shape[0])
    not_outliers = df[(df[column] >= min_val) & (df[column] <= max_val)]

    return not_outliers
```

## clean_columns <a name="clean_columns"></a> 
[Volver al índice](#indice)

As explained before, is the function that given a pandas dataframe df, 
creates a list (list_columns_to_delete) with the names of the 
columns to drop from df. 
If a column has variance zero, this is, it has a unique value, it's deleted.
As well, if 'dtime' is a column, we sort the values according to it, and if 
'Date' and 'Time' are possible columns it creates a new with the dtime.
Finally, we delete the outliers values, if wanted ([Y/N]).

```python
def clean_columns(self, df):
    """Given a dataset, it cleans its columns
    :param df: pandas dataframe
    :return: cleaned df"""

    list_columns_to_delete = []

    # In the case a column only contains one value for all samples:
    for col in df.columns:
        if df.nunique().isin([0])[col] == True:  # len(df[col].unique()) == 1:
            list_columns_to_delete.append(col)

    # Set the index the datetime
    if 'dtime' in df.columns:
        df.set_index("dtime", inplace=True)
        df.sort_values(by='dtime', inplace=True)  # Sort the values by time
        list_columns_to_delete.append('time')
    elif ('Date' in df.columns and 'Time' in df.columns):
        df['dtime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        df.set_index("dtime", inplace=True)
        list_columns_to_delete.append('Date')
        list_columns_to_delete.append('Time')
    else:
        pass

    # Outliers
    print(df.columns)
    while True:
        try:
            name_col_out = str(input("Enter the name of the column to extract the outliers:"))
            decision_outliers = str(input("Do you want to delete some outliers? [Y]/N"))
            if (name_col_out in df.columns and decision_outliers in ['Y', 'N']):
                break
            else:
                print("Try again")
        except ValueError:
            print('Invalid')
            continue
    if decision_outliers == 'Y':
        print('Proceed to delete outliers of the dataset')
        df = self.delete_outliers(df, name_col_out)

    else:
        print('Proceed to continue with outliers of the dataset')

    # Delete all the columns that we saved into the list 'list_columns_to_delete'
    df.drop(labels=list_columns_to_delete, axis='columns',
            inplace=True)  # df.drop(labels=list_columns_to_delete, axis=1, inplace=True)

    return df
```

## clean_rows <a name="clean_rows"></a> 
[Volver al índice](#indice)

Just in case there are some samples duplicated, this function
delete them.

```python
def clean_rows(self, df):
    """Given a dataset, it cleans its rows
    :param: df: pandas dataframe
    :return: cleaned df"""

    # Duplicated rows -> delete it
    dups = df.duplicated()
    # report if there are any duplicates
    print("Is there any duplicated rows?", dups.any())
    print("The number of samples duplicated are: ", df[dups].shape[0])
    df.drop_duplicates(inplace=True)
    print("The duplicated samples were deleted.")

    return df
```

## general_clean <a name="general_clean"></a> 
[Volver al índice](#indice)

This method is in charge of manage all the cleaning. So it
called the methods explained previously of the Class Preprocessing
and save into a new scv file the dataset processed.

```python
def general_clean(self, dir_path, data_name, df):
    # self.explore_dataset(df)
    self.missing_values(df)
    self.clean_columns(df)
    self.clean_rows(df)
    try:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)  # If it does not exist the directory, we create it
        df.to_csv('{}.csv'.format(os.path.join(dir_path, data_name + '_processed')))  # Save it
        print(f'Saved correctly: ' '{}.csv'.format(os.path.join(dir_path, data_name + '_processed')))
    except OSError:
        print("The name of the file or the directory are incorrect")
```


# Analyze and visualize the data <a name="Analyze"></a> 
[Volver al índice](#indice)


The class `Analyze` in the file `analysis.py` will be the one used to calculate the Moving Average and the 
Relative Strenght Index in order to graphic the values across time.
The class has four attributes, two (df and cripto) initialized when creating
an instance of the class that are the processed dataset and the currency selected.
The other two are initialized while executing the process. These are media_movil and rsi.

```python
@dataclass()
class Analyze:

    colors_plots = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    def __init__(self, df, cripto):
        self.df = df
        self.cripto = cripto

    def __post_init__(self):
        self.media_movil = None
        self.rsi: float = 0
```


The class also have nine different methods:
* get_periodos_user: extract the periods given by the user
* get_media_movil: calculate the moving average
* get_rsi: calculate the RSI
* economy: save the values in the attributes
* get_grafico_cotizaciones, get_grafico_media_movil, get_grafico_rsi, get_grafico_cotizacion_media_movil: visualize the values
obteined first across the periods selected
* graficos_pro: visualize thanks to the library `streamlit` in a new tab


## get_periodos_user <a name="get_periodos_user"></a> 
[Volver al índice](#indice)

This method will be used later on and the goal is to ask to the user the integer that
represents the pediodicity of the movity average to represent it.

```python
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
```

## get_media_movil <a name="get_media_movil"></a> 
[Volver al índice](#indice)

The moving average (MA) is a simple technical analysis tool that 
smooths out price data by creating a constantly updated average price. 
The average is taken over a specific period of time, like 10 days, 
20 minutes, 30 weeks, or any time period the trader chooses.

Given a series of numbers and a fixed subset size, the first element of the moving 
average is obtained by taking the average of the initial fixed subset of the number series. 
Then the subset is modified by "shifting forward"; that is, excluding the first number 
of the series and including the next value in the subset.

```python
def get_media_movil(self, periodos):
    """Get the media movil
    :param df: pandas dataframe
    :param periodos: int value greater than cero and less than 200 (given by the user)
    :return: a pandas series"""
    return pd.Series(pd.Series.rolling(self.df['close'], periodos).mean())
```

## get_rsi <a name="get_rsi"></a> 
[Volver al índice](#indice)

The Relative Strength Index (RSI), developed by J. Welles Wilder, is a momentum oscillator 
that measures the speed and change of price movements. The RSI oscillates between zero and 100. 
Traditionally the RSI is considered overbought when above 70 and oversold when below 30. 
Signals can be generated by looking for divergences and failure swings. RSI can also be used to 
identify the general trend.
RSI is considered overbought when above 70 and oversold when below 30. These traditional levels 
can also be adjusted if necessary to better fit the security.
The RSI is a fairly simple formula, but is difficult to explain without pages of examples. 
Refer to Wilder's book for additional calculation information. 
RSI = 100 – [100 / ( 1 + (Average of Upward Price Change / Average of Downward Price Change ) ) ].

Notice that if the input periodosRSI is not given, it's fixed to 14.

```python
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
```

## economy <a name="economy"></a> 
[Volver al índice](#indice)

This method saves the results in the attributes media_movil and rsi respectively.

```python
def economy(self):
    """Save the values in the class"""
    self.media_movil = self.get_media_movil(self.get_periodos_user())
    self.rsi = self.get_rsi()
```

## get_grafico_cotizaciones <a name="get_grafico_cotizaciones"></a> 
[Volver al índice](#indice)

The final objective is being able to visualize the values obtained with formulas.
These four methods get_grafico_cotizaciones, get_grafico_media_movil, get_grafico_rsi, get_grafico_cotizacion_media_movil return 
the graphic.

```python
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
```

## graficos_pro <a name="graficos_pro"></a> 
[Volver al índice](#indice)

This is the core method to visualize the information obtained. 
It uses the library Streamlit to project all the graphics at the same time.

```python
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
```

# Workflow <a name="workflow"></a> 
[Volver al índice](#indice)

The project is managed with `workflow.py` in which the classes are imported and the names
are defined, so it get easier for the future if it's needed to change it.

The code consists in create an instance of each class mentioned before and use the
method.
1. Extract the data
2. Read the original dataset
3. Process the data
4. Read the processed dataset
5. Calculate and graphic

```python
# Import modules and respective functions
from extract_data import *
from preprocessing import *
from analysis import *


if __name__ == "__main__":

    dir_path = 'data'
    data_name = 'dataset_to_process'
    name_file = 'Possible_Currencies'
    dataset_name = 'dataset'

    # Extract the data
    data = Get_Data()
    data.get_dataframe_to_process(dir_path, name_file, data_name)

    # Process the data
    df = pd.read_csv('{}.csv'.format(os.path.join(dir_path, data_name)))
    preprocessing = Preprocessing()
    preprocessing.general_clean('results', dataset_name, df)

    # Analysis and graphics
    df_processed = pd.read_csv('{}.csv'.format(os.path.join('results', dataset_name + '_processed')), index_col=0)
    analysis = Analyze(df_processed, data.cripto_user_selected)
    analysis.economy()
    analysis.graficos_pro()
```



--- 



# Conclusions <a name="conclusions"></a> 
[Volver al índice](#indice)

To sum up, the idea was to learn more how to carry on a simple project in a virtual
environment and upload it in Github.
The objective was to be able to manage the project as a real one, with different files
to separate the process, and with some generalization done with classes.

If you have any suggest, please do not hesitate to contact emartindedi@alumni.unav.es
and I will be pleased to answer it.