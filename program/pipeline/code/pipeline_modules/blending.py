import os
import cv2
import traceback
from pipeline.code.exceptions import get_module_logger
import pipeline.settings

fld = pipeline.settings.OUTPUT_FOLDER
beta1 = pipeline.settings.BETA1
beta2 = pipeline.settings.BETA2
basename = pipeline.settings.RUN_NAME
out_file = os.path.join(fld, basename + "_blended.tif")
logger = get_module_logger(__name__)
APP_ROOT = os.path.abspath(os.path.dirname(__file__))


def list_images(dir_):

    color_path, hill_path, slope_path = "", "", ""

    list_img = [each for each in os.listdir(dir_) if each.endswith('.tif')]
    for img in list_img:
        if "_color.tif" in img:
            color_path = os.path.join(dir_, img)
        if "_hillshade.tif" in img:
            hill_path = os.path.join(dir_, img)
        if "_slopeshade.tif" in img:
            slope_path = os.path.join(dir_, img)

    return color_path, hill_path, slope_path


def blend(color_, hill_, slope_):  # Blend images

    color = cv2.imread(color_)
    slopeshade = cv2.imread(slope_)
    hillshade = cv2.imread(hill_)

    step_1 = cv2.addWeighted(color, 1.0, slopeshade, beta1, 0.0)
    step_2 = cv2.addWeighted(step_1, (1-beta2), hillshade, beta2, 0.0)

    cv2.imwrite(out_file, step_2)


# Function to run all script logic
def run():

    try:
        print("1.- Retrieving files")
        color_, hill_, slope_ = list_images(fld)
        print("2.- Blending files")
        blend(color_, hill_, slope_)

    except Exception as error:
        print("Error creating the blended file from color, slope-shade and hill-shade files: {}.".format(error))
        logger.exception('Blending operation error')
        traceback.print_exc()
    finally:
        print("SUCCESSFULLY created the blended file from color, slope-shade and hill-shade files")
        logger.info('Ending blending module')
