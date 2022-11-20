# Import necessary libraries
import os
import pandas as pd
import krakenex
from pykrakenapi import KrakenAPI # Note: pykrakenapi requires Python >= 3.3, krakenex >= 2.0.0 and pandas

def save_currencies(dir_path, name_file):
    """save into a csv file the wsname and altname of the currencies availables in the kraken API
    : dir_path: path of the folder (directory) where it will be saved
    : name_file: name (without .csv) of the file where it will be saved"""
    try:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path) # If it does not exist the directory, we create it
        currencies = dict(zip(k.get_tradable_asset_pairs()['wsname'], k.get_tradable_asset_pairs()['altname'])) # Get the names of the currencies available
        df = pd.DataFrame.from_dict(currencies, orient='index', columns=['altname']) # Transform the dictionary into a dataframe
        df.to_csv('{}.csv'.format(os.path.join(dir_path, name_file))) # Save it
        print("Saved correctly")
    except TypeError:
        print("The name of the file or the directory are incorrect")

def ask_user_for_currency(df):
    """ask the user a currency
    : df: pandas dataframe object which contains the wsname and altname of all the currencies availables in the kraken API
    : return: a string which contains the wsname of the currency selected by the user"""
    print("The possible answers are:")
    for idx, element in enumerate(list(df.index)):
        print("{}) {}".format(idx +1 , element))
    #print("The possible answers", df.index) more simple
    while True:
        try:
            user_curr = str(input("Enter the abbreviation of the currency wanted:"))
            if user_curr in df.index:
                break
            else:
                print("The currency is not available or it not correct")
        except ValueError:
            print('Invalid')
            continue
    return user_curr

def user_select_currency(df, curr):
    """get the data available for the currency which has wsname curr
    : df: pandas dataframe object which contains the wsname and altname of all the currencies availables in the kraken API
    : curr: a string which contains the wsname of the currency selected by the user
    : return: a tuple object which contains the dataframe for the currency curr and the last time"""
    return (k.get_ohlc_data(df.loc[curr]['altname'], ascending=True))


# -------------------------------------------------------------------------
def get_dataframe_to_process(dir_path, name_file, data_name):
    # Obtain a csv file with all names of available currencies
    save_currencies(dir_path, name_file)

    # Save the currencies in a pandas dataframe
    currencies_names_df = pd.read_csv('{}.csv'.format(os.path.join(dir_path, name_file)), index_col=[0])

    # Ask the user for the currency wanted to analyze
    user_curr = ask_user_for_currency(currencies_names_df)

    try:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path) # If it does not exist the directory, we create it
        data = user_select_currency(currencies_names_df, user_curr)[0]
        print(data.shape)
        data.to_csv('{}.csv'.format(os.path.join(dir_path, data_name))) # Save it
        print("Saved correctly")
    except OSError:
        print("The name of the file or the directory are incorrect")
    return user_select_currency(currencies_names_df, user_curr)



if __name__ == "__main__":
    api = krakenex.API()  # Instance of the krakenex.API class
    k = KrakenAPI(api)  # Implements the Kraken API methods using the low-level krakenex python

    # Decide the names of the directory for the outputs and the name of the file containing the names of the currencies
    dir_path = 'data'
    name_file = 'Possible_Currencies'
    data_name = 'dataset_to_process'

    # Save the dataframe wanted by the user in a file called 'dataset_to_process.csv' in data directory
    get_dataframe_to_process(dir_path, name_file, data_name)
