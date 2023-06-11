library(xcms)
# library(camera) PB with PKG installation

# Create directory for output files
dir.create("data/xcms_processed", showWarnings = FALSE)

# parse all mzML files in the directory
mzml_files <- list.files("data/mzML_files",
                         pattern = "*.mzML",
                        full.names = TRUE)
#####################    preprocess mzML files   ####################

data <- xcmsSet(mzml_files,
                method = "centWave",
                ppm = 5,
                peakwidth = c(5, 20),
                snthresh = 10,
                mzdiff=0.01,
                prefilter = c(3, 100))

# Group peaks
data <- group(data, 
              method = "density",
              bw = 5, mzwid = 0.01,
              minfrac = 0.9,
              minsamp = 2)

# Retention time correction
data <- retcor(data,
               method = "obiwarp",
               plottype = "none")

# Group peaks after retention time correction
data <- group(data, 
              method = "density",
              bw = 5, mzwid = 0.01,
              minfrac = 0.9,
              minsamp = 2)

# Filling peaks
data <- fillPeaks(data)

#####################    camera   ####################

# Annotate isotopes and adducts
data.CAMERA <- CAMERA::annotate(set.filled, polarity = "positive")

## Export feature table for identification of analytes
features <- getPeaklist(set.CAMERA)
rownames(features) <- groupnames(data.filled)
write.csv(features, "XCMSResults/features.csv")