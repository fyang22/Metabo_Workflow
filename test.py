import pandas as pd
import pyopenms as oms

# load inhouse library
library = pd.read_csv('data/Compounds.csv', sep=',')

# drop rows with missing values
library = library.dropna()

# get data types
print(library.dtypes)

library['RT'] = library['RT']*60


print(library.columns)
print(library.head())
# Create an empty FeatureMap
feature_map = oms.FeatureMap()

# Iterate over all rows in the library

for index, row in library.iterrows():
    feature = oms.Feature()

    # Set the RT and m/z of the feature
    feature.setRT(row['RT'])
    feature.setMZ(row['m/z'])
    feature.setMetaValue('Feature_ID', row['Metabolites'])   

    # Set the charge of the feature
    feature_map.push_back(feature)

# Save the FeatureMap
output = 'feature_map.featureXML'
oms.FeatureXMLFile().store(output, feature_map)

# Load the FeatureMap
feature_map_file = 'feature_map.featureXML'
feature_map = oms.FeatureMap()
oms.FeatureXMLFile().load(feature_map_file, feature_map)

# load ms data from mzML file into MSExperiment
mzml_file = 'data/raw/Lib4_pos_75_01_16963.mzML'
spectra = oms.MSExperiment()
oms.MzMLFile().load(mzml_file, spectra)


#############################################

# Create a new MSExperiment to store the subset of spectra
subset_spectra = oms.MSExperiment()

# Iterate over features in the FeatureMap
for feature in feature_map:
    mz = feature.getMZ()
    rt = feature.getRT()

    # Find the corresponding spectrum in the MSExperiment
    for spectrum in spectra:
        if abs(spectrum.getRT() - rt) < 6:  # Adjust the tolerance as needed
            # Check if the spectrum matches the feature based on m/z
            for peak in spectrum:
                if abs(peak.getMZ() - mz) < 0.01:  # Adjust the tolerance as needed
                    # This spectrum corresponds to the feature, add it to the subset
                    subset_spectra.addSpectrum(spectrum)

                    # If you want to include MS2 spectra as well, uncomment the following lines
                    if spectrum.getMSLevel() == 2:
                         subset_spectra.addSpectrum(spectrum)

                    break  # Exit the inner loop once a match is found

# Save the subset of spectra to a new mzML file
subset_mzml_file = 'subset_spectra.mzML'
oms.MzMLFile().store(subset_mzml_file, subset_spectra)



