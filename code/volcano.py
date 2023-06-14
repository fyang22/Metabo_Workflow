import numpy as np
import pandas as pd

# define paths
input_file = 'data/volcano/volcano_pos.csv' # change the path and file name as desired

df_volcano = pd.read_csv(input_file)


# change 1st column name to 'Sample'
df_volcano = df_volcano.rename(columns={'Unnamed: 0': 'Sample'})
#print(df_volcano.head(5))
# filter df_volcano FC >2 and pvalue < 0.05
#df_volcano_filter = df_volcano[(df_volcano['FC'] > 2) & (df_volcano['raw.pval'] < 0.05)]
#print(df_volcano_filter.shape)
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

df_xcms_filter = df_xcms[df_xcms['Sample'].isin(df_volcano['Sample'])]
#print(df_xcms_filter.shape)
#print(df_xcms.shape)

# calculate the monoisotopic mass for each feature 
# use .loc[row_indexer,col_indexer]
df_xcms_filter['MonoisotopicMass'] = df_xcms_filter.loc[:, 'mzmed'] - 1.007276 # positive mode

#df_xcms_filter['MonoisotopicMass'] = df_xcms_filter.loc[:, 'mzmed'] + 1.007276 # negative mode

# write df_xcms_filter to csv file
#df_xcms_filter.to_csv('data/volcano/Feature_SI_pos.csv', index=False)



##############################################################################################
######################### find significant features in HMDB database #########################
##############################################################################################

hmdb = pd.read_csv('data/hmdb_cleanup_v02062023.csv')
print(hmdb.columns)


# find the closest monoisotopic mass in database and subset the database
def find_Chem(dataset, databse, mass_tolerance):

    #create a empty dataframe
    matched_db = pd.DataFrame(columns=databse.columns)
    # add two empty columns to the matched_hmdb
    matched_db['Sample'] = ''
    matched_db['Sample_mass'] = ''
    matched_db['Sample_mz'] = ''
    # create a empty 
    for index, row in dataset.iterrows():
        feature_mass = row['MonoisotopicMass']
        feature_name = row['Sample']
        feature_mz = row['mzmed']
        # get DB chemicals where the monoisotopic mass in hmdb database with tolerance
        # indicate error if no matched chemicals
        db_mass = databse[(databse['monisotopic_molecular_weight'] >= feature_mass - mass_tolerance) 
                          & (databse['monisotopic_molecular_weight'] <= feature_mass + mass_tolerance)]
            # add feature name to the db_mass
        db_mass['Sample'] = feature_name 
        db_mass['Sample_mass'] = feature_mass
        db_mass['Sample_mz'] = feature_mz 
        
            # add db_mass to the matched_hmdb

        matched_db = matched_db._append(db_mass)
            #matched_db['Sample'] = feature_name
            #matched_db['Sample_mass'] = feature_mass
            
    return matched_db

matched_hmdb = find_Chem(df_xcms_filter, hmdb, 0.01)
print(matched_hmdb.shape)
print(matched_hmdb.head(5))


# calculate the mass difference between feature mass and hmdb mass as ppm
matched_hmdb['delta_mass(ppm)'] = ((matched_hmdb['monisotopic_molecular_weight'] - 
                                   matched_hmdb['Sample_mass']).abs())/ matched_hmdb['monisotopic_molecular_weight'] * 1e6

# check delta_mass(ppm) < 5 ppm
#matched_hmdb_select = matched_hmdb[matched_hmdb['delta_mass(ppm)'] <= 10]

#print(matched_hmdb_select.shape)
#print(matched_hmdb_select.head(5))
print(matched_hmdb.shape)
#print(matched_hmdb.head(5))
#matched_hmdb.to_csv('data/volcano/match_neg.csv', index=False)
#matched_hmdb_select.to_csv('data/volcano/match_5ppm_neg.csv', index=False)