import numpy as np
import pandas as pd

# define paths
input_file = 'data/volcano/volcano_pos.csv' # change the path and file name as desired

df_volcano = pd.read_csv(input_file)


# change 1st column name to 'Sample'
df_volcano = df_volcano.rename(columns={'Unnamed: 0': 'Sample'})
#print(df_volcano.head(5))
# filter df_volcano FC >2 and pvalue < 0.05
df_volcano_filter = df_volcano[(df_volcano['FC'] > 2) & (df_volcano['raw.pval'] < 0.05)]
print(df_volcano_filter.shape)
print(df_volcano.shape)

# find the common features between volcano and xcms feature table
# read xcms feature table
input_xcms_file = 'data/xcms_processed/output_Final-positive.tsv' # change the path and file name as desired
df_xcms = pd.read_table(input_xcms_file,
                            delim_whitespace=True,
                            index_col=0)
# change columns name
df_xcms = df_xcms.rename(columns={'name': 'Sample'})

# subset df_xcms with df_volcano_filter by values in Sample column

df_xcms_filter = df_xcms[df_xcms['Sample'].isin(df_volcano_filter['Sample'])]
print(df_xcms_filter.shape)
print(df_xcms.shape)

# write df_xcms_filter to csv file
df_xcms_filter.to_csv('data/volcano/Feature_SI.csv')

