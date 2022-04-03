# Program Pipeline -* Visualization of spectral series *-

## Introduction

This Python code uses terrain visualization techniques in combination with
spectral analysis results on paleoclimate proxy time series.

The purpose of this novel program is to produce a bespoke visualization using time (x), period (y) 
and power spectrum (z), extracted from multiple time series files that have been previously generated 
using non-evolutive spectral methods. The output of this program resembles those graphs from evolutive
spectral analysis, such as wavelet, aiming for a quick view, better user experience and more accurate 
interpretation of the results.

The research domain in which this program best fits into is the earth sciences, especially geology.
In particular, the study of time series becomes useful for analysing and interpreting the past climate
and all its facets. This tool can help researchers who are familiar with spectral methods such as 
Lomb-Scargle, but have not yet approach the data for investigating its spectral evolution over time.

## Prerequisites

This project has been tested using python 3.7.0 in a Windows environment. In principle, there 
are no constrains on migrating to other systems (i.e. Linux) and/or to higher versions of Python.
The most important libraries in the program are the following ones (including the used version):

numpy==1.21.2
matplotlib==3.1.2

Both of them are included in the 'requirements.txt' file.

However, there are two mandatory requirements:

- *GDAL utilities*: The program needs the GDAL utilities (https://gdal.org/) to be fully operative 
  in the command line of the operative system, as the program will make direct calls to these 
  (i.e. `C:\>gdal_translate`). Installing the GDAL library in Python is not a requirement.
  
- *Python 2 and mapnik library*: The program also needs Python 2 to be installed in the
computer machine and to be callable from the command line (i.e. `C:\>python2`). The reason 
  for this is that the mapnik library (https://mapnik.org/) which this program uses for the 
  blending operation, needs a 32-bit installation of Python27. This is required to run Mapnik.
  An example of how to install Mapnik can be found here:
  https://github.com/mapnik/mapnik/wiki/WindowsInstallation
  
## Overview

The 'pipeline_manager' script controls the flow of the 4 modules of the program:

* **1. create_asc.py**: Reads the data files and produces a raster file in ASCII-format (*.asc).
* **2. gdal_steps.py**: Generates the color-relief, slope and hillshade in GTiff format (*.tif)
  from the .asc file.
* **3. mapnik_blending.py**: it blends all the three previous raster files into one.
* **4. plotting.py**: Adds extra visual elements for interpretation.

## Input files

Three types of files are needed per time sub-series for running the program. The program comes with
sample data by default for the user to test it.

* *Files with extension .LOM*: It is a space-delimited file with two columns, one for the frequencies and
one for the power spectrum.
* *Files with extension .ACL*: It is a space-delimited file with two columns, one for the frequencies and
one for achieved confidence level.
* *Files with extension .prn*: It is a space-delimited file with two columns containing the data, one 
  for the time (i.e. years, kilo-years, etc.) and one for the values of the proxy time series.
  
For best results, the time sub-series should be split from the original time series before the spectral
analysis, as this must be carried out on each sub-series. The time series can have uneven sampling, 
but ideally with the same time length, and with an overlapping between consecutive time sub-series 
higher than 50%. This way, the visualization becomes more effective.

## Configuration

If the **settings.py** is not configured/updated, the program will produce by default a series 
of files in the 'output' folder and based on the sample data that is available in the 'data' folder,
which corresponds to 2,015 spectral analysis on 2,015 time sub-series extracted from a 
Pliocene-Pleistocene synthesized benthic delta-O-18 dataset (Lisiecki and Raymo, 2005). 

This is the list of params, that can be changed:

* *ACHIEVED_CONFIDENCE_LEVEL*: 95 by default (0-100). It represents the achieved confidence level (ACL)
  of the spectral analysis by which the frequencies are displayed in the output raster. The values 
  of ACL that are below this limit will be treated as no-data values.
  
* *HIGHEST_FREQUENCY_TO_EVALUATE*: 0.06 by default. It represents the maximum frequency that was evaluated
during the spectral analysis. Each time sub-series have this value as the last frequency value.
  
* *LOWEST_FREQUENCY_TO_EVALUATE*: 0.00 by default. It represents the minimum frequency that was evaluated
during the spectral analysis. Each time sub-series have this value as the first frequency value.
  
* *NUMBER_OF_FREQUENCIES*: 500 by default. It represents the number of values between the maximum
frequency and the minimum frequency that were evaluated during the spectral analysis on each time
   sub-series.
  
* *NODATA*:  -999 by default. It represents the pixel value of those raster values below the marked
 achieved confidence level, this will be saved as the no-data values in the output raster.
  
* *REMOVE_TEMP*: True by default. It indicates whether the auxiliary files that are generated 
  in the intermediate stages are deleted (True) or preserved (False) in the output folder.
  
* *DATA_FOLDER*: The relative path of the subfolder where the input files are located.

* *RUN_NAME*: The basename of the output file and intermediate files. The program will also attach 
  the timestamp to it.
  
* *template_filename *: Any filename of the time sub-series corresponding to the proxy values (.prn).
This is for quality and validation purposes.
  
* *search_expression *: Search expression must be contained in all input files.

* *tile_plot *: The tile of the final plot.

The other parameters do not need to be changed. Even if the color template file 
(i.e. color-ramp-PW-stack) is updated, the filename does not need to be adjusted.
  
## Run Instructions

- Download the program folder.
- Navigate to the main folder.
- Type in the console: `python debug_runner.py run_code`

The program will generate the output into the output folder.

## Directory Structure
* **pipeline**: Contains all pipeline and settings.py that contains the configuration variables.
* **.gitignore**
* **debug_runner.py**
