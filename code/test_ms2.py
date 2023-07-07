from pyopenms import *
import numpy as np
import os
import pymzml
import matplotlib.pyplot as plt
import pandas as pd
import glob

def extract_ion_chromatogram_pymzml(mzml_file, mz, mz_tol):
    run = pymzml.run.Reader(mzml_file)

    times = []
    intensities = []

    for spectrum in run:
        if spectrum.ms_level == 1:  # process MS1 spectra
            for i, mz_i in enumerate(spectrum.mz):
                if mz - mz_tol <= mz_i <= mz + mz_tol:
                    times.append(spectrum.scan_time[0])
                    intensities.append(spectrum.i[i])

    return times, intensities

def plot_chromatogram(times, intensities,feature, save_dir):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(times, intensities)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Intensity")
    ax.set_title(feature)
    #ax.set_xticks(np.arange(0, max(times), 100))
    ax.set_xticks(np.arange(0, 1200, 100))
    fig.savefig(os.path.join(save_dir, f'{feature}.png'), dpi=300)
    plt.close(fig)

def export_msms(mzml_file, mz, rt, mz_tol, rt_tol,output_file):#mz_min, mz_max, rt_min, rt_max, output_file):
    # Load the mzML file
    exp = MSExperiment()
    MzMLFile().load(mzml_file, exp)


    ms2_found = False  
    #no_ms2 = []
    # Loop through the spectra in the file
    for spectrum in exp.getSpectra():
        # Check if the spectrum is an MS2 spectrum
        if spectrum.getMSLevel() == 2:
            # Get the precursor 
            precursor = spectrum.getPrecursors()[0]
            precursor_mz = precursor.getMZ()
            precursor_rt = spectrum.getRT()

                # Check if the precursor matches m/z and RT 
            if np.any(abs(precursor_mz - mz) <= mz_tol) and np.any(abs(precursor_rt - rt) <= rt_tol):
                ms2_found = True  # Set the flag to True if MS2 is found
                peak_mz, intensity = spectrum.get_peaks()
                peaks = np.column_stack((peak_mz, intensity))
                peaks = peaks[(peaks[:,0] <= mz)]
                peaks = peaks[peaks[:,1].argsort()[::-1]]
                peaks = peaks[:10]
                with open(output_file, 'w') as f:
                    for m, i in peaks:
                        m = m.round(4)
                        f.write(f'{m}\t{i}\n')      
    if not ms2_found:
        print(f"No MS2 data found for the feature {feature}.")

                    # # Save the precursor ion and MS/MS in an mgf file
                    # mgf_exp = MSExperiment()
                    # mgf_exp.addSpectrum(spectrum)
                    # MascotGenericFile().store(mgf_file, mgf_exp)  
   
mz_tol = 0.005  # m/z tolerance Da TODO: use mz_min and mz_max from the feature table same for rt
rt_tol = 6  # RT tolerance in seconds 

# Load the mzML file containing the MS2 spectra
mzml_file = glob.glob('data/raw/*.mzML')
output_dir = "data/output_neg"
save_dir = "data/chromatogram_neg"
df = pd.read_csv('data/Feature/CompoundList_neg.csv',delimiter=',')

for file in mzml_file:
    print('Loadfile: ', file)
    for index, row in df.iterrows():
        feature = row['Sample']
        mz = row['Sample_mz'] 
        # mz_min = row['Sample_mz_min']
        # mz_max = row['Sample_mz_max']
        # rt_min = row['Sample_rt_min']
        # rt_max = row['Sample_rt_max']    
        # replace with mz_min and mz_max from the feature table
        rt = row['Sample_rt']
        file_name = row['Sample_max']
        if file_name == os.path.basename(file)[:-5]: # map the file with sample_max
            print('Export MSMS for feature: ', feature)
            output_file = os.path.join(output_dir,os.path.basename(file).split('_')[0] + '_' + f'{feature}' + '.txt')
            export_msms(file, mz, rt, mz_tol, rt_tol, output_file)
            # plot chromatogram
            times, intensities = extract_ion_chromatogram_pymzml(file, mz, mz_tol)
            plot_chromatogram(times, intensities, feature, save_dir)