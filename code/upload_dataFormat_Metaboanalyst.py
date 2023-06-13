################################################################################################################
################                                                                                ################
################                                                                                ################
################    This is a script to generate a csv file for SERRF statistic processing      ################
################                                                                                ################
################                                                                                 ################
################################################################################################################

# import libraries
import numpy as np
import pandas as pd

#define paths
input_file = 'data/xcms_processed/output_Final-negative.tsv' # change the path and file name as desired

# output file path for metaboanalyst
metabo_output_path = 'data/xcms_processed/metaboanalyst_datafile_neg.csv' # change the path and file name as desired

# read tsv file
data_xcms = pd.read_table(input_file,
                          delim_whitespace=True,
                          index_col=0)

# change the file based on MetaboAnalyte template
# modify columns name by each datafile
datafile = data_xcms.rename(columns={'name': 'Sample'})

# subset the datafile with columns contain sample names and Sample
datafile = datafile.filter(regex='Sample|QC|WT|KO')
for col in datafile.columns:
    if col == 'Sample': # keep Sample column
        continue
    elif '_' not in col: # remove columns with replicate number
        datafile = datafile.drop(col, axis=1)
    

# get sample categories and groups based on column names
def get_sample_categories(datafile):
    # categories = {}
    group_names = []
    subgroup_names = []
    
    for col in datafile.columns:
        if col == 'Sample':
            continue
        elif '-' in col and 'QC' not in col:
            group_name = col.split('-')[0]
            subgroup_name = col.split('-')[:1] if len(col.split('-')) > 1 else ''
            label = col.split('-')[:2] if len(col.split('-')) > 2 else ''
            group_names.append(group_name)
            subgroup_names.append(subgroup_name)
        elif 'QC' in col:
            group_name = 'QC'
            subgroup_name = 'QC'
            group_names.append(group_name)
            subgroup_names.append(subgroup_name)
    return  group_names, subgroup_names

# run function
group_names, subgroup_names = get_sample_categories(datafile)

# create group and subgroup rows (op)
# group_rows = pd.Series(['Sample'] + list(group_names)) (optional)
subgroup_rows = pd.Series(['Sample'] + list(subgroup_names))

# copy the datafile 
datafile_metaboanalyst = datafile.copy()

# and add group and subgroup rows to the datafile
# datafile_metaboanalyte.loc[-1] = group_rows (optional)
datafile_metaboanalyst.loc[-2] = subgroup_rows

#print(datafile.head(5))

# save data for metaboanalyst
metabo_output_path = 'data/xcms_processed/metaboanalyte_datafile_neg.csv' # change the path and file name as desired
datafile_metaboanalyst.to_csv(metabo_output_path, index=False)
