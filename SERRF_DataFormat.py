################################################################################################################
################                                                                                ################
################                                                                                ################
################    This is a script to generate a csv file for SERRF statistic processing      ################
################                                                                                ################
################                                                                                ################
################################################################################################################

# import libraries
import numpy as np
import pandas as pd

#define paths
input_file = 'data/xcms_processed/output_Final-negative.tsv' # change the path and file name as desired

# output file path for metaboanalyst
metabo_output_path = 'data/xcms_processed/metaboanalyst_datafile_neg.csv' # change the path and file name as desired

# output file path for serrf
##### serrf output file index name 'No' position need to be modified ########
serrf_output_path = 'data/xcms_processed/serff_datafile_neg.csv' # change the path and file name as desired

# read tsv file
data_xcms = pd.read_table(input_file,
                          delim_whitespace=True,
                          index_col=0)

# check reading data
# print(data_xcms.head(5))

# check columns names
# note the name need to be modified and clean up

# print(data_xcms.columns)


# change the file based on MetaboAnalyte template
# modify columns name by each datafile
datafile = data_xcms.rename(columns={'name': 'Sample'})

print(datafile.shape)
# remove features with retention time < 90s
datafile = datafile[datafile['rtmed'] > 90]
print(datafile.shape)
# print(datafile.columns)

# get subdf with ion counts
df_ioncount = datafile.filter(regex='Sample|QC|WT|KO')
for col in df_ioncount.columns:
    if len(col.split('_')) < 3: # remove columns with replicate number
        df_ioncount = df_ioncount.drop(col, axis=1)

print(df_ioncount.shape)
# print(df_ioncount.columns)

# if all the values in a row are <10000, remove the row 
df_ioncount = df_ioncount[(df_ioncount.iloc[:, 1:] > 10000).any(axis=1)]
print(df_ioncount.shape)
# subset the datafile with df_ioncount by index
datafile = datafile.loc[df_ioncount.index]
print(datafile.shape)


# # subset the datafile with columns contain sample names and Sample
# datafile = datafile.filter(regex='Sample|QC|WT|KO')
# for col in datafile.columns:
#     if col == 'Sample': # keep Sample column
#         continue
#     elif '_' not in col: # remove columns with replicate number
#         datafile = datafile.drop(col, axis=1)
    
# ############################## upload data format to SERRF format ############################################
# datafile_serff = datafile.copy()

# # order the columns by last string in the column name

# datafile_serff = datafile_serff.reindex(sorted(datafile_serff.columns, 
#                                                key=lambda x: x.split('_')[-1] if x != 'Sample' else x), 
#                                                axis=1)

# # keep the Sample column at the first column
# datafile_serff = datafile_serff[['Sample'] + [col for col in datafile_serff.columns if col != 'Sample']]

# #### !set index column PB index name position
# # index = [i for i in range(1, len(datafile_serff.index)+1)]
# # datafile_serff.index = pd.Index(index, name='No')

# # adapt the multiindex format for SERRF
# # batch: A, A, A,..
# batch = ['batch'] + ['A'] * (len(datafile_serff.columns)-1)
# ## print(batch)

# # sampleType according to the column name (QC, sample)
# sampleType = []
# for col in datafile_serff.columns:
#     if 'Sample' in col:
#         sampleType.append('sampleType')
#     elif 'QC' in col:
#         sampleType.append('qc')
#     else:
#         sampleType.append('sample')
# ## print(len(sampleType))
# # time: injection order (1, 2, 3, ...)
# time = ['time'] + [i for i in range(1, len(datafile_serff.columns))]
# ## print(len(time))
# # label: sample name
# label = ['label'] + [col for col in datafile_serff.columns if col != 'Sample']
# ## print(len(label))



# # create multiiindex for the datafile skip the index column
# datafile_serff.columns = pd.MultiIndex.from_arrays([batch, sampleType, time, label],
#                                                     #names=['batch', 'sampleType', 'time', 'label'],
#                                                     )
                                                    
# # add an index column with name 'No' and start from 1
# datafile_serff.insert(0, 'No', range(1, 1 + len(datafile_serff))) 
               

# # save to csv file
# #datafile_serff.to_csv(serrf_output_path, index=False)
# print(datafile_serff.shape)
# #print(datafile_serff.head(5))