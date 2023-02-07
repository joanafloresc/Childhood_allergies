import pandas as pd
from sklearn.preprocessing import PowerTransformer

def ptransform_data(df):
    '''function that operates PowerTransformer in x'''

    df_copy = df.copy().astype('float32')
    
    transformer = PowerTransformer()
    transformer.fit(df_copy)
    
    df_tr = transformer.transform(df_copy)
    df_tr = pd.DataFrame(df_tr, columns = df_copy.columns)
    
    return df_tr
