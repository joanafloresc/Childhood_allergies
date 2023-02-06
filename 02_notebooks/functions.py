import math
import pandas
import matplotlib.pyplot as plt
import seaborn as sns

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
