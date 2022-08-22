import subprocess
import pipeline.code.pipeline_modules.create_asc as asc
import pipeline.code.pipeline_modules.gdal_steps as gdal_transformations
import pipeline.code.pipeline_modules.blending as blending
import pipeline.code.pipeline_modules.plotting as plot

from pipeline.code.exceptions import get_module_logger

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


def create_spectral_visualization():

    asc.run()
    gdal_transformations.run()
    blending.run()
    plot.run()


def run_option(requested_stage):

    switcher = {"run_code": lambda: create_spectral_visualization()}

    return switcher.get(requested_stage, lambda: "Error: Requested option is invalid")()
