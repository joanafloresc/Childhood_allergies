import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def mmscale_data(df):
    '''function that operates MinMaxScaler in x'''

    df_copy = df.copy().astype('float32')
    
    scaler = MinMaxScaler()
    scaler.fit(df_copy)
    
    df_sc = scaler.transform(df_copy)
    df_sc = pd.DataFrame(df_sc, columns = df_copy.columns)
    
    return df_sc

def sscale_data(df):
    '''function that operates MinMaxScaler in x'''

    df_copy = df.copy().astype('float32')
    
    scaler = StandardScaler()
    scaler.fit(df_copy)
    
    df_sc = scaler.transform(df_copy)
    df_sc = pd.DataFrame(df_sc, columns = df_copy.columns)
    
    return df_sc
