# import libraries
import pandas as pd
import numpy as np

# read in the volcano data
df = pd.read_csv('data/volcano/Feature_SI.csv')

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
df_print.to_csv('data/Feature/check_chroma.csv', index=False)
# count the number of each sample
df_count = df_print['Sample_max'].value_counts()
print(df_count)
print(df_count)

