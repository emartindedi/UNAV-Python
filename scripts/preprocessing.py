# Import necessary libraries
import os
import pandas as pd
import numpy as np
import krakenex
from pykrakenapi import KrakenAPI # Note: pykrakenapi requires Python >= 3.3, krakenex >= 2.0.0 and pandas.


def explore_dataset(df):
    # The names of the columns are:
    print("The columns are:", df.columns)
    print("There are ", df.shape[1], " columns on the dataset and ", df.shape[0], "samples")
    print(df.nunique())
    print(df.isna().any())
    # Descriptive Statistics
    stats = df.describe(include='all', datetime_is_numeric=True)
    print(stats)



def preprocessing(df):
    #explore_dataset(df)
    #clean_columns(df)
    #clean_values(df)


if __name__ == "__main__":

    dir_path = 'data'
    data_name = 'dataset_to_process'

    df = pd.read_csv('{}.csv'.format(os.path.join(dir_path, data_name)))

    preprocessing(df)










