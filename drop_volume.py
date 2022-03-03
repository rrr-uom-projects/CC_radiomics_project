# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 10:08:22 2021

@author: chelmis3

 Script drops features that highly correlate with volume ie: Spearman's Rank
 correlation coefficient of >= 0.9
 
 A list of highly correlating features is created and used to in a drop()
 function on the main dataframe (data_path).
 The resulting dataframe is saved in a new csv file (out_path)
"""

from __future__ import print_function
import pandas as pd
import pingouin as pg

def find_corr(data_path, out_path, corr_vol):
    # data setup
    pd_data = pd.read_csv(data_path)

    data_f = pd_data.loc[:, (pd_data.columns.str.startswith("original_") |
                             pd_data.columns.str.startswith("log-sigma") |
                             pd_data.columns.str.startswith("wavelet-"))]

    df = pd.DataFrame(data_f)
    df = df.astype(float)
    
    d_stats = pg.pairwise_corr(df, columns=['original_shape_MeshVolume'],
                               method='spearman', tail='one-sided')
    
    #save correlation values in a csv
    d_stats.to_csv(corr_vol, index=False)
    # filter_df contains list of columns highly correlating to volume
    filter_df = d_stats[(d_stats['r']).abs() >= 0.9]
    # create a list
    drop_cols = filter_df['Y'].tolist()
 
    # create dataframe
    new_data = pd_data.drop(drop_cols, axis=1)
    new_data.to_csv(out_path, index=False)
    
      
# paths
find_corr(path_to_csv_file_with_radiomic_features,
          path_to_csv_file_after_radiomic_features_highly_correlated_to_volume_are_dropped,
          path_to_csv_file_showing_feature_correlations_to_volume)
