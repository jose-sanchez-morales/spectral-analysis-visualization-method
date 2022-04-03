# -*- coding: utf-8 -*-

import os
import traceback
import subprocess

import pipeline.settings
from pipeline.code.exceptions import get_module_logger

logger = get_module_logger(__name__)
APP_ROOT = os.path.abspath(os.path.dirname(__file__))

nodata = pipeline.settings.NODATA
out_folder = pipeline.settings.OUTPUT_FOLDER
prn_path = pipeline.settings.DATA_FOLDER
color_template_path = pipeline.settings.COLOR_FILE_TEMPLATE
slopeshade_template_path = pipeline.settings.SLOPESHADE_FILE_TEMPLATE
basename = pipeline.settings.RUN_NAME
asc_file = os.path.join(out_folder, basename + ".asc")
tif_file = os.path.join(out_folder, basename + ".tif")
color_tif = os.path.join(out_folder, basename + "_color.tif")
slope_tif = os.path.join(out_folder, basename + "_slope.tif")
hillshade = os.path.join(out_folder, basename + "_hillshade.tif")
slopeshade_tif = os.path.join(out_folder, basename + "_slopeshade.tif")


def execute(command):
    print('Executing: ' + command)
    try:
        command_line_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        process_output, _ = command_line_process.communicate()
        print('execution done')
        logger.debug(process_output)

    except OSError as exception:
        logger.error('Exception occurred: ' + str(exception))
        logger.error('Subprocess failed: ' + command)
        raise
    return True


def asc_to_tif(input_f, output_f):
    try:
        command = "gdal_translate " \
                  "-of GTiff " \
                  "-a_nodata " + str(nodata) + " -ot Float32 -a_srs EPSG:27700 " + input_f + " " + output_f

        execute(command)

        logger.debug("Translating .asc into .tif")

        return True
    except Exception as e:
        logger.debug("Exception at translating .asc: " + str(input_f) + " " + str(e))
        return False


def tif_to_color(input_f, color_path, output_f):

    try:
        command = "gdaldem color-relief " \
                  "-of GTiff " + input_f + " " + color_path + " " + output_f

        execute(command)

        logger.debug("Adding color-ramp into .tif")

        return True
    except Exception as e:
        logger.debug("Exception at adding color-ramp into .tif: " + input_f + " " + str(e))
        return False


def tif_to_slope(input_f, output_f):

    try:
        command = "gdaldem slope -of GTiff " + input_f + " " + output_f

        execute(command)

        logger.debug("Generating slope raster from .tif")

        return True
    except Exception as e:
        logger.debug("Exception at generating slope raster from .tif: " + input_f + " " + str(e))
        return False


def slope_to_color(input_f, color_path, output_f):

    try:
        command = "gdaldem color-relief " \
                  "-of GTiff " + input_f + " " + color_path + " " + output_f

        execute(command)

        logger.debug("Adding color-ramp into .tif")

        return True
    except Exception as e:
        logger.debug("Exception at adding color-ramp into .tif: " + input_f + " " + str(e))
        return False


def tif_to_hillshade(input_f, output_f):

    try:
        command = "gdaldem hillshade " \
                  "-of GTiff " + input_f + " " + output_f

        execute(command)

        logger.debug("Generating hillshade raster from .tif")

        return True
    except Exception as e:
        logger.debug("Exception at generating hillshade raster from .tif: " + input_f + " " + str(e))
        return False


def run():

    try:

        print("1.- Translating .asc into .tif")
        asc_to_tif(asc_file, tif_file)

        print("2.- Adding color into .tif")
        tif_to_color(tif_file, color_template_path, color_tif)

        print("3.- Generating slope raster")
        tif_to_slope(tif_file, slope_tif)

        print("4.- Adding color shade into slope raster")
        slope_to_color(slope_tif, slopeshade_template_path, slopeshade_tif)

        print("5.- Generating hillshade raster")
        tif_to_hillshade(tif_file, hillshade)

    except Exception as error:
        print("Error creating the GTiff, color, slope, hillshade files from ASCII grid file: {}.".format(error))
        logger.exception('GTiff creation error')
        traceback.print_exc()
    finally:
        print("SUCCESSFULLY created the GTiff, color, slope, hillshade files from ASCII grid file")
        logger.info('Ending GDAL steps module')
