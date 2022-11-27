# Import necessary libraries
import os
import pandas as pd
import numpy as np
from numpy import percentile
import datetime
from datetime import datetime

def explore_dataset(df):
    """Function that print some information about the dataset.
    : df: pandas dataframe"""
    # The names of the columns are:
    print("The columns are:", df.columns)
    print("There are ", df.shape[1], " columns on the dataset and ", df.shape[0], "samples")
    print("", df.nunique())
    print(df.isna().any())
    print(type(df.isna().any()))
    # Descriptive Statistics
    stats = df.describe(include='all', datetime_is_numeric=True)
    print(stats)


def missing_values(df):
    """Function that given a dataset it creates a list with the columns that have some missing values. Then if there is not empty, the user
        is asked for the method to use.
    : df: pandas dataframe
    : return: the cleaned dataset with the method selected by the user: delete, mean or median are the options"""
    list_columns_missing = list()
    for col in df.columns:
        n_miss = df[col].isnull().sum() # count number of rows with missing values
        if n_miss > 0:
            list_columns_missing.append(col)
    if len(list_columns_missing)!=0:
        print("The columns with missing values are:", list_columns_missing)
        while True:
            try:
                method_missing = str(input("Choose a method for the missing values: delete, mean, median"))
                if method_missing in ['delete']:
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


def get_percentile(df, percentile_rank, column):
    """Given a dataset and the column to calculate the percentile 75 and 25, it calculates the index position
    : df : pandas dataframe
    : percentile_rank: generally 75 or 25, a value between 0 and 100
    : column: valid name column of the dataframe df
    : return: the element in the index and column passed"""

    # First, sort by ascending columns, reset the indices
    df = df.sort_values(by=column).reset_index()
    index = (len(df.index) - 1) * percentile_rank / 100.0
    index = int(index)
    return df.at[index, column]


def delete_outliers(df, column,  k=1.5):
    """Given a dataset and the name of a column it calculates the outlier cutoff and identify the outliers
    : df: pandas dataframe
    : column: valid name column of the dataframe df
    : k: contant (int) generally 1.5
    : return: the cleaned dataframe without outliers"""
    # Compute the 25th percentile, the 75th percentile and the IQR
    p25 = get_percentile(df, 25, column)
    p75 = get_percentile(df, 75, column)
    # calculate interquartile range
    iqr = p75 - p25

    # calculate the outlier cutoff
    # "Minimum non-outlier value": 25th percentile - 1.5 * IQR
    min_val = p25 - k * iqr
    # "Maximum non-outlier value": 75th percentile + 1.5 * IQR
    max_val = p75 + k * iqr
    print(f"The outlier cutoff is {min_val, max_val}")
    #print(f"The outlier cutoff is {min_val, max_val}", min_val, max_val)

    # identify outliers
    outliers = df[(df[column] < min_val) | (df[column] > max_val)]
    print('Identified outliers: %d' % outliers.shape[0])
    not_outliers = df[(df[column] >= min_val) & (df[column] <= max_val)]

    return not_outliers



def clean_columns(df):
    """Given a dataset, it cleans its columns.
    : df: pandas dataframe
    : return: cleaned df"""

    list_columns_to_delete = []

    # In the case a column only contains one value for all samples:
    for col in df.columns:
        if df.nunique().isin([0])[col] == True: # len(df[col].unique()) == 1:
            list_columns_to_delete.append(col)


    # Set the index the datetime
    if 'dtime' in df.columns:
        df.set_index("dtime", inplace=True)
        df.sort_values(by='dtime', inplace=True) # Sort the values by time
        print(df.head(3))
        list_columns_to_delete.append('time')
    elif ('Date' in df.columns and 'Time' in df.columns):
        df['dtime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        df.set_index("dtime", inplace=True)
        print(df.head(3))
        list_columns_to_delete.append('Date')
        list_columns_to_delete.append('Time')
    else:
        pass

    # Outliers

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
        delete_outliers(df, name_col_out)
        #print(delete_outliers(df, name_col_out))
    else:
        print('Proceed to continue with outliers of the dataset')

    #print(list_columns_to_delete)
    # Delete all the columns that we saved into the list 'list_columns_to_delete'
    df.drop(labels=list_columns_to_delete, axis='columns', inplace=True) #df.drop(labels=list_columns_to_delete, axis=1, inplace=True)

    return df


def clean_rows(df):
    """Given a dataset, it cleans its rows.
    : df: pandas dataframe
    : return: cleaned df"""

    # Duplicated rows -> delete it
    dups = df.duplicated()
    # report if there are any duplicates
    print("Is there any duplicated rows?", dups.any())
    print("The number of samples duplicated are: ", df[dups].shape[0])
    df.drop_duplicates(inplace=True)
    print("The duplicated samples were deleted.")

    return df


def preprocessing(df):

    #explore_dataset(df)

    clean_columns(df)

    clean_rows(df)

    missing_values(df)




if __name__ == "__main__":

    dir_path = 'data'
    data_name = 'dataset_to_process'

    df = pd.read_csv('{}.csv'.format(os.path.join(dir_path, data_name)))
    dff = df.copy() # Optional

    preprocessing(dff)






