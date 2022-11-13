# Import necessary libraries
import os
import pandas as pd
import numpy as np
import krakenex
from pykrakenapi import KrakenAPI # Note: pykrakenapi requires Python >= 3.3, krakenex >= 2.0.0 and pandas.


def get_currencies(dir_path, name_file):
    """"""
    try:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        currencies = dict(zip(k.get_tradable_asset_pairs()['wsname'], k.get_tradable_asset_pairs()['altname']))
        df = pd.DataFrame.from_dict(currencies, orient='index', columns=['altname'])
        df.to_csv('{}.csv'.format(os.path.join(dir_path, name_file)))
        print("Saved correctly")
    except TypeError:
        print("The name of the file or the directory are incorrect")

def ask_user_for_currency(dir_path, name_file, df):
    print("The possible answers are:")
    for idx, element in enumerate(list(df.index)):
        print("{}) {}".format(idx +1 , element))
    # print("The possible answers", data.index) more simple
    while True:
        try:
            user_curr = str(input("Enter the abbreviation of the currency wanted:"))
            if user_curr in df.index:
                break
            else:
                print("The currency is not available or it not correct.")
        except ValueError:
            print('Invalid')
            continue
    return user_curr

def user_select_currency(dir_path, name_file, df, curr):
    """"""
    return (k.get_ohlc_data(df.loc[curr]['altname'], ascending=True))
#


# -------------------------------------------------------------------------

if __name__ == "__main__":
    api = krakenex.API()  # Instance of the krakenex.API class
    k = KrakenAPI(api)  # Implements the Kraken API methods using the low-level krakenex python

    dir_path = 'results'
    name_file = 'Possible_Currencies'

    get_currencies(dir_path, name_file)

    currencies_names_df = pd.read_csv('{}.csv'.format(os.path.join(dir_path, name_file)), index_col=[0])

    user_curr = ask_user_for_currency(dir_path, name_file, currencies_names_df)

    (cur1, cur2) = user_select_currency(dir_path, name_file, currencies_names_df, user_curr)

    print(cur1.head())
    print(cur1.tail())


