import pandas as pd

df = pd.read_csv('data/volcano/match_pos.csv',delimiter=',')
df_filter = df[df['delta_mass(ppm)'] <= 5]
#print(df_filter.columns)
# print accesion number
#print(df_select.shape)
# read in the volcano data
df_sample = pd.read_csv('data/volcano/Feature_SI_pos.csv')

#subset the date with columns contain sample names
df_sample = df_sample.filter(regex='Sample|WT-|KO-|QC_', axis=1)
#print(df_sample.columns)
# compare the values in each row and find the max value and add its sample name to the new column
df_sample['Sample_max'] = df_sample.idxmax(axis=1,numeric_only=True)
# print(df_sample.shape)
# select unique compounds drop the one with larger delta_mass(ppm)
df_filter = df_filter.sort_values(by=['delta_mass(ppm)'], ascending=True)
df_filter_unique = df_filter.drop_duplicates(subset=['Sample'], keep='first')
# print(df_filter.shape)
# print(df_filter_unique.shape)

# assigne the sample_max to the unique compounds based on the sample name
#sample_file = []
for index, row in df_filter_unique.iterrows():
    sample = row['Sample']
    sample_max = df_sample.loc[df_sample['Sample'] == sample, 'Sample_max'].iloc[0]
    df_filter_unique.loc[index, 'Sample_max'] = sample_max
    # print(sample_max)
    # sample_file.append(sample_max)
# print(df_filter_unique.head(5))
# print(df_filter_unique.shape)

# drop row with Sample_max contain 'QC'
df_filter_unique_extract = df_filter_unique[df_filter_unique['Sample_max'].str.contains('QC')== False]
print(df_filter_unique_extract.shape)

# save to csv file
df_filter_unique_extract.to_csv('data/Feature/CompoundList.csv', index=False)