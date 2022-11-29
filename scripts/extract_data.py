# Import necessary libraries
import os
import pandas as pd
import time
import krakenex
from pykrakenapi import KrakenAPI # Note: pykrakenapi requires Python >= 3.3, krakenex >= 2.0.0 and pandas
from dataclasses import dataclass

"""Module to extract data"""


@dataclass()
class Get_Data:
    def __post_init__(self):
        self.cripto_user_selected = ''


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
            print("The name of the file or the direc'{}.csv''{}.csv'tory are incorrect")

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

    def user_select_currency(self, curr):
        """get the data available for the currency which has wsname curr
        : df: pandas dataframe object which contains the wsname and altname of all the currencies availables in the kraken API
        : curr: a string which contains the wsname of the currency selected by the user
        : return: a tuple object which contains the dataframe for the currency curr and the last time"""
        api = krakenex.API()  # Instance of the krakenex.API class
        k = KrakenAPI(api)
        interval = 60
        time.sleep(5)
        return (k.get_ohlc_data(curr, ascending=True, interval=interval))


    def get_dataframe_to_process(self, dir_path, name_file, data_name):
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
            print(data.shape)
            data.to_csv('{}.csv'.format(os.path.join(dir_path, data_name)))  # Save it
            print(f'Saved correctly: ' '{}.csv'.format(os.path.join(dir_path, data_name)))
        except OSError:
            print("The name of the file or the directory are incorrect")
        return self.user_select_currency(self.cripto_user_selected)

