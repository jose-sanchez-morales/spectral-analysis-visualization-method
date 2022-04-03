import os
import time

# absolute path for the root of the application
APP_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
capture = time.strftime("%Y%m%d_%H%M%S")

# Variables that inform the ASCI file creation:
ACHIEVED_CONFIDENCE_LEVEL = 95
HIGHEST_FREQUENCY_TO_EVALUATE = 0.06
LOWEST_FREQUENCY_TO_EVALUATE = 0.00
NUMBER_OF_FREQUENCIES = 500
NODATA = -999
REMOVE_TEMP = False

# Changing params
DATA_FOLDER = os.path.join(APP_ROOT, r"pipeline\data\subseries_stack_combined")
#DATA_FOLDER = os.path.join(APP_ROOT, r"pipeline\data\subseries_insolation_combined")
RUN_NAME = "d18stack_assesment_" + capture
#RUN_NAME = "Insolation_assesment_" + capture
template_filename = "d18-0001.prn"
#template_filename = "las0001.prn"
search_expression = "d18"
#search_expression = "las"
tile_plot = "LR04 Global Pliocene-Pleistocene Benthic $δ^{18}O$ Stack Power Spectra" #$ italics
#tile_plot = "Summer insolation at 65°N on June 21 Power Spectra"

# FIXED variables
OUTPUT_FOLDER = os.path.join(APP_ROOT, r"pipeline\output")
PROJECTION_FILE_TEMPLATE = os.path.join(APP_ROOT, r"pipeline\templates\projection_file.prj")
COLOR_FILE_TEMPLATE = os.path.join(APP_ROOT, r"pipeline\templates\color-ramp-PW-stack.clr")
SLOPESHADE_FILE_TEMPLATE = os.path.join(APP_ROOT, r"pipeline\templates\color_slope.txt")
MAPNIK_TEMPLATE = os.path.join(APP_ROOT, r"pipeline\templates\mapnik_template.xml")
MAPNIK_FOLDER = os.path.join(APP_ROOT, r"pipeline\code\pipeline_modules")
