# import libraries
import pandas as pd
import numpy as np

# read in the volcano data
df = pd.read_csv('data/volcano/Feature_SI_pos.csv')

# subset the date with columns contain sample names
df_sample = df.filter(regex='WT-|KO-|QC_', axis=1)

# compare the values in each row and find the max value and add its sample name to the new column
df['Sample_max'] = df_sample.idxmax(axis=1)
#print(df.shape)
#print(df.columns)
# select columns to print
df_print = df[['Sample', 'mzmed', 'rtmed','Sample_max',]]
# sort by Sample_max
df_print = df_print.sort_values(by=['Sample_max'])
df_print.to_csv('data/Feature/check_chroma_pos.csv', index=False)