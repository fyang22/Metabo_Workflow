# import libraries
import numpy as np
import pandas as pd

## todo: data path ##
# load hmdb database
hmdb = pd.read_csv('data/hmdb.csv')

# load feature table
data = pd.read_csv('data/sig_feauture.csv')

# calculate monoisotopic mass
mH = 1.007276
# positive mode
data['monoisotopic_mass'] = (data['mzmed'] - mH)

# negative mode
#data['monoisotopic_mass'] = (data['mzmed'] + mH)

# mapping the feature table to hmdb database with monoisotopic mass

# find the closest monoisotopic mass in hmdb database

for index, row in data.interrows():

    feature_mass = row['monoisotopic_mass']
    feature_name = row['name']
    # get hmdb chemicals where the monoisotopic mass in hmdb database with tolerance 0.005 Da
    hmdb_mass = hmdb[(hmdb['monoisotopic_molecular_weight'] >= feature_mass - 0.005) & (hmdb['monoisotopic_molecular_weight'] <= feature_mass + 0.005)]

    # concat all the possible chemicals as a table
    hmdb_mass = pd.concat([hmdb_mass]*len(feature_mass), ignore_index=True)
    return hmdb_mass

# calculate the mass difference between feature mass and hmdb mass as ppm
hmdb_mass['delta_mass(ppm)'] = (hmdb_mass['monoisotopic_molecular_weight'] - feature_mass) / feature_mass * 1e6








