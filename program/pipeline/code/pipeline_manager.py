import subprocess
import os
import pipeline
import pipeline.code.pipeline_modules.create_asc as asc
import pipeline.code.pipeline_modules.gdal_steps as gdal_transformations
import pipeline.code.pipeline_modules.plotting as plot

from pipeline.code.exceptions import get_module_logger
from pipeline.settings import MAPNIK_FOLDER
mapnik_script = os.path.join(MAPNIK_FOLDER, "mapnik_blending.py")

# Set up logging object
logger = get_module_logger(__name__)


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


def run_mapnik(script_path):

    try:

        print("7.- Blending color, slopeshade and hillshade using mapnik and Python2")

        x = len(asc.all_time)
        y = pipeline.settings.NUMBER_OF_FREQUENCIES

        template_file = pipeline.settings.MAPNIK_TEMPLATE
        basename = pipeline.settings.RUN_NAME
        out_folder = pipeline.settings.OUTPUT_FOLDER

        python2_command = 'python2 ' + script_path + ' ' \
                          + template_file + ' ' \
                          + basename + ' ' \
                          + out_folder + ' ' \
                          + str(x) + ' ' \
                          + str(y)

        print(python2_command)
        execute(python2_command)

        logger.debug("Blending color, hillshade and slopeshade using mapnik library")

    except Exception as e:
        logger.debug("Exception at Blending color, hillshade and slopeshade using mapnik library " + str(e))


def create_spectral_visualization():

    asc.run()
    gdal_transformations.run()
    run_mapnik(mapnik_script)
    plot.run()


def run_option(requested_stage):

    switcher = {"run_code": lambda: create_spectral_visualization()}

    return switcher.get(requested_stage, lambda: "Error: Requested option is invalid")()
