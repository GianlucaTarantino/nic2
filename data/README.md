# Data

In this folder are contained al the csv of the EEG signal detected by the Mega2560.

**File format**: Files are in the csv format and each line contains the y value at the line sample number of the EEG signal.

## raw
This folder contains all the data detections without any filter or cross-correlation. These are the relevated data as they are outputted by the Mega2560.

**Naming convention**: \<id\>\_\<number of the relevation\>\_\<date\>.csv

## processed
This folder contains all the data detections, with applied low pass, high pass and notch filters. The filters are applied as follows:
- Low Pass: 15Hz
- High Pass: 0.35Hz
- Notch Filter: 50Hz
- 
**Naming convention**: \<id\>\_\<number of the relevation\>\_\<date\>.csv

## interim_samples
This folder contains all the single movements, taken from the processed files.

**Naming convention**: \<number of the sample\>\_\<id\>\_\<number of the relevation\>\_\<date\>.csv

## samples
Mean signal of all the signals of the same type in interim_samples. These are the samples used for the cross correlation.

**Naming convention**: \<signal type\>\_sample.csv
