import ipywidgets as widgets
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

def dataset_overview(dataset):

    out_overview = widgets.Output()
    out_stats_num = widgets.Output()
    out_stats_cat = widgets.Output()
    out_stats_date = widgets.Output() # new
    out_dtypes = widgets.Output()
    out_unique = widgets.Output()
    out_missing_plot = widgets.Output()

    with out_overview:
        num_variables = dataset.shape[1]
        num_observations = dataset.shape[0]
        missing = dataset.isnull().sum().sum()
        missing_per_col = dataset.isnull().sum()
        missing_perc = (100*(missing_per_col/len(dataset))).mean().round(2)
        duplicate_rows = dataset.duplicated().sum()
        duplicate_rows_perc = (100*(duplicate_rows/len(dataset))).round(2)
        zeros_count = dataset[dataset==0].count(axis=0).sum()
        zeros_count_per_col = dataset[dataset==0].count(axis=0)
        zeros_count_perc = 100*(zeros_count_per_col/len(dataset)).mean().round(2)
        data_overview = pd.DataFrame([num_variables,num_observations,missing,missing_perc,duplicate_rows,duplicate_rows_perc,zeros_count,zeros_count_perc],
                          index=['Number of variables','Number of observations','Missing values','Missing values (%)','Duplicate rows','Duplicate rows (%)','Zeros','Zeros (%)'],columns=[''])
        data_overview.index.name='Dataset overview'
    
        data_overview_round=data_overview.T.round(decimals=pd.Series([0, 0, 0, 3, 0, 3,0,3], index=data_overview.index)).T
        data_overview_round = data_overview_round.astype(object) 
        display(data_overview_round)
    
    with out_stats_num:
        data_stats_num = pd.DataFrame(dataset.describe(exclude=['object','datetime','timedelta'])).T
        data_stats_num_round_style = data_stats_num.style.set_caption('Descriptive statistics (numerical)').set_precision(2)
        display(data_stats_num_round_style)
        
    with out_stats_cat:
        data_cat = []
        for k in dataset.columns:
            if (dataset[k].dtype=='object') | (dataset[k].dtype=='str'):
                data_stats_cat = pd.DataFrame(dataset.describe(exclude=['number','datetime', 'timedelta'])).T
                data_stats_cat_style = data_stats_cat.style.set_caption('Descriptive statistics (categorical)')
                display(data_stats_cat_style)
                break
        else:
            display('No categorical columns in this dataset')
            
        
    with out_stats_date:
        data_dates = []
        for k in dataset.columns: 
            if np.issubdtype(dataset[k].dtype, np.datetime64):  
                subset = dataset.loc[:,k]
                data_stats_date = subset.describe(include=['datetime','timedelta'])
                data_dates.append(data_stats_date)     
        
        data_dates_df = pd.DataFrame(data_dates)
        #data_dates_df.index.names = ['Variables']
        display(data_dates_df)  
        
               
                
    with out_dtypes:
        num_dtypes = dataset.select_dtypes(exclude=['object','datetime', 'timedelta']).dtypes.count()
        cat_dtypes = dataset.select_dtypes(exclude=['number','datetime', 'timedelta']).dtypes.count()
        data_dtypes = dataset.select_dtypes(include=['datetime','timedelta']).dtypes.count()
        data_types = pd.DataFrame([num_dtypes,cat_dtypes,data_dtypes],index=['Numeric','Categorical','Date'],columns=[''])
        data_types.index.name='Variable types'
        display(data_types)
        
    with out_unique:
        col_names_unique = []
        description = []
        columns = []
        for row,column in enumerate(dataset.columns):
            unique_values = dataset[column].nunique()
            count_values = dataset[column].dropna().unique()
    
            if len(count_values) <= 12:
                columns.append(column)
                col_names_unique.append(unique_values)
                description.append(count_values)
            else:
                columns.append(column)
                col_names_unique.append(unique_values)
                description.append(count_values[:15])
        
        
        unique_df = pd.DataFrame([columns,col_names_unique,description]).T
        unique_df.columns = ['Features','count_unique','unique']
        #display(unique_df)
        
        dtypes = pd.DataFrame(dataset.dtypes, columns=['Data Types'])
        dtypes = dtypes.reset_index()
        dtypes.columns = ['Features', 'Data Types']
        dtype_col = dtypes['Data Types']
        unique_df = pd.concat([unique_df,dtype_col],axis=1)
        display(unique_df)
        
    with out_missing_plot:
        missing_per_col_plot = dataset.isnull().sum()
        non_missing_per_col_plot = len(dataset)-missing_per_col_plot # add
        missing_perc_plot = (100*(missing_per_col_plot/len(dataset))).round(2) # add
        non_missing_perc_plot = 100 - missing_perc_plot # add
        missing_df = pd.DataFrame([missing_perc_plot,non_missing_perc_plot]).T
        missing_df.columns = ['missing','not_missing']
        
        fig = go.Figure(data=[
        go.Bar(name='Missing', x=missing_df.index, y=missing_df['missing']),
        go.Bar(name='Not Missing', x=missing_df.index, y=missing_df['not_missing'])])
        # Change the bar mode
        fig.update_layout(barmode='stack',title='Missing values', xaxis_title="Features",yaxis_title="Percentage (%)")
        fig.show()

#         labels = missing_df.index
#         cm = plt.get_cmap('nipy_spectral')

#         fig,ax=plt.subplots(figsize=(10,6))

#         ax.bar(labels, missing_df['missing'], label='Missing')
#         ax.bar(labels, missing_df['not_missing'], label='Not Missing',bottom=missing_df['missing'])
#         ax.legend()
#         plt.xticks(labels, rotation='vertical')
#         ax.set_ylim([0, 100])
#         ax.set_ylabel('Percentage')
#         ax.set_xlabel('Categorical Features')
#         ax.set_title('Visualization Missing values')
#         plt.show()

 
    
    hbox = widgets.HBox([out_overview,out_dtypes,out_missing_plot],layout={'border': 'red','width':'100%'})
    hbox2 = widgets.HBox([out_stats_num])
    hbox3 = widgets.HBox([out_stats_cat])
    hbox4 = widgets.HBox([out_unique])
    hbox5 = widgets.HBox([out_stats_date])
    #vbox = widgets.VBox([hbox,hbox2,hbox3])

    tab = widgets.Tab(children=[hbox,hbox4,hbox2,hbox3,hbox5])
    tab.set_title(0,'Data Overview')
    tab.set_title(1,'Unique Values')
    tab.set_title(2,'Descriptive Stats (Num)')
    tab.set_title(3,'Descriptive Stats (Cat)')
    tab.set_title(4,'Descriptive Stats (Date)')
    #return display(vbox)
    return display(tab)
