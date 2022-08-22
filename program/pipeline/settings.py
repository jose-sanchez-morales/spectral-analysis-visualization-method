import os
import time

# absolute path for the root of the application
APP_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
capture = time.strftime("%Y%m%d_%H%M%S")

# Variables that inform the ASCI file creation:
ACHIEVED_CONFIDENCE_LEVEL = 0  # i.e., 95
HIGHEST_FREQUENCY_TO_EVALUATE = 0.06
LOWEST_FREQUENCY_TO_EVALUATE = 0.00
NUMBER_OF_FREQUENCIES = 500
# NUMBER_OF_FREQUENCIES = 250
NODATA = -999
REMOVE_TEMP = False
BETA1 = 0.1  # range from 0 to 1; opacity for first blend (slopeshade raster and color raster file)
BETA2 = 0.4  # range from 0 to 1; opacity for second blend (hillshade raster file and first blend)

# Changing params
# DATA_FOLDER = os.path.join(APP_ROOT, r"pipeline\data\untuned_stack_combined")
# DATA_FOLDER = os.path.join(APP_ROOT, r"pipeline\data\subseries_stack_combined")
DATA_FOLDER = os.path.join(APP_ROOT, r"pipeline\data\subseries_insolation_combined")
# RUN_NAME = "d18stack_assessment_" + capture
RUN_NAME = "Insolation_assessment_" + capture
# template_filename = "uLR0001.prn"
# template_filename = "d18-0001.prn"
template_filename = "las0001.prn"
# search_expression = "uLR"
# search_expression = "d18"
search_expression = "las"
# tile_plot = "LR04 untuned Global Pliocene-Pleistocene Benthic $δ^{18}$O Stack Power Spectra (ACL> " \
# + str(ACHIEVED_CONFIDENCE_LEVEL) + " %)"  # $ italics
# tile_plot = "LR04 Global Pliocene-Pleistocene Benthic $δ^{18}$O Stack Power Spectra (ACL> " \
# + str(ACHIEVED_CONFIDENCE_LEVEL) + " %)"  # $ italics
tile_plot = "Summer insolation at 65°N on June 21 Power Spectra (ACL> " \
             + str(ACHIEVED_CONFIDENCE_LEVEL) + " %)"

# FIXED variables
OUTPUT_FOLDER = os.path.join(APP_ROOT, r"pipeline\output")
PROJECTION_FILE_TEMPLATE = os.path.join(APP_ROOT, r"pipeline\templates\projection_file.prj")
COLOR_FILE_TEMPLATE = os.path.join(APP_ROOT, r"pipeline\templates\color-ramp-PW-stack.clr")
SLOPESHADE_FILE_TEMPLATE = os.path.join(APP_ROOT, r"pipeline\templates\color_slope.txt")
HILLSHADE_FILE_TEMPLATE = os.path.join(APP_ROOT, r"pipeline\templates\color_hill.txt")
