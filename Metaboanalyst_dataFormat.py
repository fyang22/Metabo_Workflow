import re
import pandas as pd
import numpy as np

#define paths
input_file = 'data/xcms_processed/output_Final-positive.tsv' # change the path and file name as desired

# output file path for metaboanalyst
metabo_group_output_path = 'data/xcms_processed/metaboanalyst_group_pos.csv' # change the path and file name as desired
metabo_subgroup_output_path = 'data/xcms_processed/metaboanalyst_subgroup_pos.csv' # change the path and file name as desired


df = pd.read_table(input_file,
                          delim_whitespace=True,
                          index_col=0)

# find regular expression in column names
df = df.rename(columns={'name': 'Sample'})

# remove features with retention time < 90s
df = df[df['rtmed'] > 90]
print(df.shape)
# print(datafile.columns)

# get subdf with ion counts
df_ioncount = df.filter(regex='Sample|QC|WT|KO')
for col in df_ioncount.columns:
    if len(col.split('_')) < 3: # remove columns with replicate number
        df_ioncount = df_ioncount.drop(col, axis=1)

print(df_ioncount.shape)
# print(df_ioncount.columns)

# if all the values in a row are <10000, remove the row 
df_ioncount = df_ioncount[(df_ioncount.iloc[:, 1:] > 10000).any(axis=1)]
print(df_ioncount.shape)
# subset the datafile with df_ioncount by index
df = df.loc[df_ioncount.index]
print(df.shape)



df = df.filter(regex='Sample|QC|WT|KO')
for col in df.columns:
    if col == 'Sample': # keep Sample column
        continue
    elif len(col.split('_')) < 3: # remove columns with replicate number
        df  = df.drop(col, axis=1)


def select_col(col_name, group_name):
    if group_name[0] in col_name:
        if len(col_name.split('-')) > 2:
            return col_name
    elif group_name[1] in col_name:
        if len(col_name.split('-')) > 2:
            return col_name
    elif group_name[2] in col_name:
        if len(col_name.split('_')) > 1:
            return col_name
    elif 'Sample' in col_name:
        return col_name


group = ['WT', 'KO', 'QC']
select_col_name = [select_col(col, group) for col in df]
df = df.filter([i for i in select_col_name if i is not None], axis=1)

# Define a function to map column names to data categories
def get_subgroup(col_name, group_name):
    for i in group:
        if i == 'QC':
            if i in col_name:
                return 'QC'
        else:
            if i in col_name:
                return i + '-' + col_name.split("-")[1]

##############################################################################################################
            
# get group name WT, KO, QC ONLY
def get_group(col_name, group_name):
    for i in group:
        if i == 'QC':
            if i in col_name:
                return 'QC'
        else:
            if i in col_name:
                return i


# Create a new row to define data categories based on the column names
subgroup_row = pd.Series(data=[get_subgroup(col, group) for col in df.columns],
                            index=df.columns)

group_row = pd.Series(data=[get_group(col, group) for col in df.columns],
                            index=df.columns)

# Append the category row to the dataframe
df_subgroup = df._append(subgroup_row, ignore_index=True)
df_group =df._append(group_row, ignore_index=True)

# move the category row to the first row
def move_row(df):
    # get datafile row
    target_row = df.shape[0] - 1
    # Move target row to first element of list.
    idx = [target_row] + [i for i in range(len(df)) if i != target_row]
    df = df.iloc[idx].reset_index(drop=True)
    df.loc[0,'Sample'] = 'Label'
    return df
# move the category row to the first row
df_subgroup = move_row(df_subgroup)
df_group = move_row(df_group)

print(df_subgroup.head(5))
print(df_group.head(5))
print(df_subgroup.shape)

df_subgroup.to_csv(metabo_subgroup_output_path, index=False)
df_group.to_csv(metabo_group_output_path, index=False)
