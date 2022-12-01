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
