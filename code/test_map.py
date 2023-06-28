import pandas as pd
import glob
import os

ms2_files = glob.glob('data/output/*.txt')
df = pd.read_csv('data/Feature/CompoundList.csv',delimiter=',')

precursor_mz = pd.DataFrame(columns=['Sample_max', 'Sample','Sample_mz','Sample_rt','accession','monisotopic_molecular_weight'])

for file in ms2_files:
    file_name = os.path.basename(file).split('.')[0] 
    feature = file_name.split('_')[1]

    for index, row in df.iterrows():
        if row['Sample'] == feature:
            precursor_mz = precursor_mz._append({'Sample_max':file_name, 'Sample':row['Sample'],'Sample_mz':row['Sample_mz'],'Sample_rt':row['Sample_rt'],'accession':row['accession'],'monisotopic_molecular_weight':row['monisotopic_molecular_weight']}, ignore_index=True)

print(precursor_mz)
precursor_mz.to_csv('data/output/precursor_mz.csv', index=False)
