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

# calculate the monoisotopic mass for each feature
df_xcms_filter['MonoisotopicMass'] = df_xcms_filter['mzmed'] - 1.007276 # positive mode
# df_xcms_filter['MonoisotopicMass'] = df_xcms_filter['mzmed'] + 1.007276 # negative mode





##############################################################################################
######################### find significant features in HMDB database #########################
##############################################################################################

# hmdb = pd.read_csv('data/hmdb.csv')
# print(hmdb.columns)

# find the closest monoisotopic mass in database and subset the database
def find_Chem(dataset, databse, mass_tolerance):
    for index, row in dataset.iterrows():
        feature_mass = row['MonoisotopicMass']
        feature_name = row['Sample']
        # get DB chemicals where the monoisotopic mass in hmdb database with tolerance
        db_mass = databse[(databse['monoisotopic_molecular_weight'] >= feature_mass - mass_tolerance) 
                          & (databse['monoisotopic_molecular_weight'] <= feature_mass + mass_tolerance)]
        # add feature name to the db_mass
        db_mass['Sample'] = feature_name
        
        # concat all the possible chemicals as a table
        db_mass = pd.concat([db_mass]*len(feature_mass), ignore_index=True)
        db_mass = pd.concat(db_mass, ignore_index=True)
    return db_mass

# matched_hmdb = find_Chem(df_xcms_filter, hmdb, 0.005)
# print(matched_hmdb.shape)
# print(matched_hmdb.head(5))

# # calculate the mass difference between feature mass and hmdb mass as ppm
# matched_hmdb['delta_mass(ppm)'] = (matched_hmdb['monoisotopic_molecular_weight'] - 
#                                    matched_hmdb['MonoisotopicMass']) / matched_hmdb['MonoisotopicMass'] * 1e6



