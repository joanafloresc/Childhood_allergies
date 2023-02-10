
import pandas as pd

def std_column_name(df):
    '''function that lower cases and removes redundant words of column names'''
    
    df_copy = df.copy()
    col = list(df.columns)
    new_col = []
    
    for c in col:
        c = c.lower().replace('alg_','')
        new_col.append(c)
    df_copy.columns = new_col
    return df_copy

def negative_values(df):
    '''function that replaces negative values by 0 in allergies columns'''
    
    df_copy = df.copy()
    
    allerg_list = ['shellfish', 'fish', 'milk', 'soy', 'egg', 'wheat', 'peanut', 'sesame', 'treenut',
              'walnut', 'pecan', 'pistach', 'almond', 'brazil', 'hazelnut', 'cashew', 'atopic', 'allergic']
    
    allerg_list = [c for c in df_copy.columns if c.split('_')[0] in allerg_list]
    
    df_copy[allerg_list] = df_copy[allerg_list].mask(df_copy[allerg_list]<0, other=0)
    
    return df_copy

def joining_nuts(df):
    '''function to join the following allergies data into nut_start and nut_end
    treenut, walnut, pecan, pistach, almond, brazil, hazelnut, cashew'''
    
    nut_list = ['treenut','walnut','pecan','pistach','almond','brazil','hazelnut','cashew']
    start_list = []
    end_list = []

    df_copy = df.copy()
    
    for d in df.columns:
        if d.split('_')[0] in nut_list:
            if 'start' in d:
                start_list.append(d)
            else:
                end_list.append(d)
    
    delete_list = start_list + end_list
    
    df_copy['nut_start'] = df_copy[start_list].sum(axis=1)
    df_copy['nut_start'] = df_copy['nut_start'].mask(df_copy['nut_start']==0, other = None)
    
    df_copy['nut_end'] = df_copy[end_list].sum(axis=1)
    df_copy['nut_end'] = df_copy['nut_end'].mask(df_copy['nut_end']==0, other = None)
    
    return df_copy, delete_list

def nut_count(df):
    '''function that counts nut allergies per subject:
    treenut, walnut, pecan, pistach, almond, brazil, hazelnut, cashew'''
    
    nut_list = ['treenut','walnut','pecan','pistach','almond','brazil','hazelnut','cashew']
    
    df_copy=df.copy()

    nut_start = [d for d in df_copy.columns if d.split('_')[0] in nut_list and 'start' in d]
    nut_end = [d for d in df_copy.columns if d.split('_')[0] in nut_list and 'end' in d]

    df_copy['nut_c_s'] = df_copy[nut_start].count(axis=1)
    df_copy['nut_c_e'] = df_copy[nut_end].count(axis=1)
    
    return df_copy

def allergy_count(df):
    '''function that counts food allergies per subject:
    shellfish, fish, milk, soy, egg, wheat, peanut, sesame, 
    treenut, walnut, pecan, pistach, almond, brazil, hazelnut, cashew'''
    
    df_copy = df.copy()

    allerg_start = [d for d in df_copy.columns if 'start' in d][1:-4]
    allerg_end = [d for d in df_copy.columns if 'start' in d][1:-4]

    df_copy['allerg_c_s'] = df_copy[allerg_start].count(axis=1)
    df_copy['allerg_c_s'] = df_copy[['allerg_c_s','nut_c_s']].sum(axis=1)

    df_copy['allerg_c_e'] = df_copy[allerg_end].count(axis=1)
    df_copy['allerg_c_e'] = df_copy[['allerg_c_e','nut_c_e']].sum(axis=1)
    
    return df_copy
import math
import matplotlib.pyplot as plt
import seaborn as sns

def plot_countplot(df, column_list):
    '''Function to plot countplots for categorical dataframe:
    2 columns, n rows (number of columns of dataframe) '''
    
    plt_size = math.ceil(len(column_list)/2)  #define rows in subplot
    n = 0 #counter to attribute position for plot
    
    col_num = []
    row_num = []
    for i1 in [0,1]:
        for i2 in list(range(0,plt_size)):
            col_num.append(i1)
            row_num.append(i2)
    
    fig, ax = plt.subplots(plt_size,2, figsize=(20,40))
    
    #orient = orientation
    
    for i in column_list:
        sns.histplot(data = df, x = i, ax = ax[row_num[n],col_num[n]], color='#a1c9f4')    
        n += 1
                      
    plt.show()

def plot_age_allergy(df,plot_list):
    '''function to plot age of allergy diagnosis per food allergy '''
    
    fig, ax = plt.subplots(figsize=(10,5))
    
    for d in plot_list:
        a = df[df[d] >= 0]['age_start_years']
        sns.histplot(a, stat='percent', element='poly', fill=False, ax=ax)
    plt.legend(labels= [c.split('_')[0] for c in plot_list])
    plt.show()

def plot_boxplot(df):
    '''Function to plot boxplots for dataframe:
    2 columns, n rows (number of columns of dataframe) '''
     
    col_names = list(df)
    
    plt_size = math.ceil(len(col_names)/2)  #define rows in subplot
    n = 0 #counter to attribute position for plot
    
    #loop to attribute positions in rows and columns
    col_num = [] 
    row_num = []
    for i1 in [0,1]:
        for i2 in list(range(0,plt_size)):
            col_num.append(i1)
            row_num.append(i2)
       
    fig, ax = plt.subplots(plt_size,2, figsize=(10,30))
    
    #loop to plot boxplots
    for i in col_names:
        sns.boxplot(data = df[i], orient = 'h', color='#a1c9f4', ax = ax[row_num[n],col_num[n]])
        ax[row_num[n],col_num[n]].set_ylabel(i)
        n += 1
                                                        
    plt.show()

def remove_outliers(df):
    '''function to remove outliers outside of 3x standard deviation'''
    
    df_copy = df.copy()
    
    col_names = list(df.columns)
    std = [] #list to store each row mean
    mean_m = [] #list to store each column mean
    
    #storing mean and std in lists    
    for i in col_names: 
        std.append (3*df_copy[i].std())
        mean_m.append (df_copy[i].mean())
    
    #creating dataframe with rows to be excluded. can't do automatically rows to be included as that would excluded Nan
    for c,s,m in zip(col_names,std,mean_m):
        df_remove = df_copy[ ( df_copy[c] < m-s ) | ( df_copy[c] > m+s) ]
    
    #removing rows to be excluded from dataframe
    df_copy = df_copy.drop(df_remove.index, axis=0)
    
    return df_copy

from sklearn.preprocessing import PowerTransformer

def ptransform_data(df):
    '''function that operates PowerTransformer in x'''

    df_copy = df.copy().astype('float32')
    
    transformer = PowerTransformer()
    transformer.fit(df_copy)
    
    df_tr = transformer.transform(df_copy)
    df_tr = pd.DataFrame(df_tr, columns = df_copy.columns)
    
    return df_tr, transformer

from sklearn.preprocessing import MinMaxScaler

def mmscale_data(df):
    '''function that operates MinMaxScaler in x'''

    df_copy = df.copy().astype('float32')
    
    scaler = MinMaxScaler()
    scaler.fit(df_copy)
    
    df_sc = scaler.transform(df_copy)
    df_sc = pd.DataFrame(df_sc, columns = df_copy.columns)
    
    return df_sc, scaler
