# -*- coding: utf-8 -*-

import os
import traceback
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
from matplotlib.colors import to_rgb

import pipeline.settings
import pipeline.code.pipeline_modules.create_asc as asc
from pipeline.code.exceptions import get_module_logger


remove = pipeline.settings.REMOVE_TEMP
high_f = pipeline.settings.HIGHEST_FREQUENCY_TO_EVALUATE
low_f = pipeline.settings.LOWEST_FREQUENCY_TO_EVALUATE
nrows = pipeline.settings.NUMBER_OF_FREQUENCIES
color_file = pipeline.settings.COLOR_FILE_TEMPLATE
this_title = pipeline.settings.tile_plot
acl = pipeline.settings.ACHIEVED_CONFIDENCE_LEVEL
f_step = -(high_f/nrows)  # negative sign (-); Graph displays HIGH f top, and LOW f bottom

out_folder = pipeline.settings.OUTPUT_FOLDER
basename = pipeline.settings.RUN_NAME
input_tif = os.path.join(out_folder, basename + "_blended.tif")
input_png = os.path.join(out_folder, basename + "_blended.png")
out_png = os.path.join(out_folder, basename + "_FINAL_" + str(acl) + "ACL.png")

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


def remove_intermediate_files(out_f):
    if remove is True:
        for root, dirs, files in os.walk(out_f):
            for filename in files:
                if "FINAL" not in filename:
                    to_remove = os.path.join(root, filename)
                    os.remove(to_remove)


def tif_to_png(input_f, output_f):
    try:

        command = "gdal_translate " + \
                  "-of PNG " + \
                  input_f + " " + output_f

        execute(command)

        logger.debug("Translating blended file (.tif) into .png")

        return True
    except Exception as e:
        logger.debug("Exception at translating .tif: " + input_f + " " + str(e))
        return False


def create_visualization(new_png_file, out_png_f):

    print(new_png_file)
    print(out_png_f)

    image = mpimg.imread(new_png_file)

    fig, ax = plt.subplots()

    ax.imshow(image)

    all_years = asc.all_time

    # x axis
    xlabels = []

    for label in all_years:
        label = label / 1000
        label = "{:.5f}".format(round(label, 5))
        if label not in xlabels:
            xlabels.append(label[0:5])

    ax.set_xticks(np.linspace(0, image.shape[1], len(xlabels))[::30])
    ax.set_xticklabels(xlabels[::30], rotation=90, size=5)

    # Set horizontal lines

    # labels pos
    pos_x = all_years.index(min(all_years, key=lambda x: abs(x - 4500)))  # ka

    y_pos = (1/23)*nrows/high_f
    plt.axhline(y=nrows - y_pos, color='green', linewidth=0.3, linestyle=':')  # 1/23ka
    plt.text(pos_x, nrows - y_pos, '23 kyr', rotation=0, fontsize=5)

    y_pos = (1 / 19) * nrows / high_f
    plt.axhline(y=nrows - y_pos, color='green', linewidth=0.3, linestyle=':')  # 1/19ka
    plt.text(pos_x, nrows - y_pos, '19 kyr', rotation=0, fontsize=5)

    y_pos = (1 / 41) * nrows / high_f
    plt.axhline(y=nrows - y_pos, color='green', linewidth=0.3, linestyle=':')  # 1/41ka
    plt.text(pos_x, nrows - y_pos, '41 kyr', rotation=0, fontsize=5)

    y_pos = (1 / 100) * nrows / high_f
    plt.axhline(y=nrows - y_pos, color='green', linewidth=0.3, linestyle=':')  # 1/100ka
    plt.text(pos_x, nrows - y_pos, '100 kyr', rotation=0, fontsize=5)

    # strong forcing but weak response
    limit_min = all_years.index(min(all_years, key=lambda x: abs(x - 1300)))
    limit_max = all_years.index(min(all_years, key=lambda x: abs(x - 1800)))
    pos_ = ((limit_max - limit_min) / 4) + limit_min
    plt.text(pos_, 465, '1.3-1.8 Ma', rotation=0, fontsize=5)
    limit_min = limit_min / 2014.5
    limit_max = limit_max / 2014.5
    plt.axhline(y=470, xmin=limit_min, xmax=limit_max, color='black', linewidth=0.5, linestyle='-')

    # weak forcing but strong response
    limit_min = all_years.index(min(all_years, key=lambda x: abs(x - 2300)))
    limit_max = all_years.index(min(all_years, key=lambda x: abs(x - 3000)))
    pos_ = ((limit_max - limit_min) / 4) + limit_min
    plt.text(pos_, 465, '2.3-3.0 Ma', rotation=0, fontsize=5)
    limit_min = limit_min / 2014.5
    limit_max = limit_max / 2014.5
    plt.axhline(y=470, xmin=limit_min, xmax=limit_max, color='black', linewidth=0.5, linestyle='-')

    # y axis
    ylabels = []

    print(round(high_f, 6))
    print(round(low_f, 6))
    print("{:.5f}".format(round(f_step, 5)))

    for label in np.arange(high_f, low_f, float("{:.5f}".format(round(f_step, 5)))):
        label = "{:.6f}".format(round(label, 6))
        if label not in ylabels:
            ylabels.append(label[0:6])

    ax.set_yticks(np.linspace(0, image.shape[0], len(ylabels))[::30])
    ax.set_yticklabels(ylabels[::30], rotation=0, size=5)

    ax.set_xlabel(" Time series CENTER expressed as Time BP (Ma) ", fontsize=7)
    ax.set_ylabel(" Frequency ", fontsize=7)

    limit1 = all_years.index(min(all_years, key=lambda x: abs(x - 2580)))  # ka
    limit1_label = all_years.index(min(all_years, key=lambda x: abs(x - 2590)))  # extra 10 ka
    plt.axvline(x=limit1, color='blue', linewidth=0.5)
    plt.text(limit1_label, 420, 'Pliocene-Pleistocene (2.58 Ma)', rotation=90, fontsize=5)

    limit2 = all_years.index(min(all_years, key=lambda x: abs(x - 892)))  # ka
    limit2_label = all_years.index(min(all_years, key=lambda x: abs(x - 902)))  # extra 10 ka
    plt.axvline(x=limit2, color='yellow', linewidth=0.5)
    plt.text(limit2_label, 315, 'MPT (0.892-0.942 Ma)', rotation=90, fontsize=5)

    limit3 = all_years.index(min(all_years, key=lambda x: abs(x - 942)))  # ka
    plt.axvline(x=limit3, color='yellow', linewidth=0.5)

    title = this_title
    plt.title(title, fontdict={'fontsize': 8})

    # Add legend
    colors = {}
    values = {}
    i = 1

    with open(color_file, 'r') as f:
        next(f)
        next(f)
        for line in f:
            print(line)
            triplet = []
            val, r_, g_, b_ = line.split()
            triplet.append(int(r_) / 255)
            triplet.append(int(g_) / 255)
            triplet.append(int(b_) / 255)
            colors[i] = triplet
            values[i] = str(val)
            i += 1

    patch_1 = mpatches.Patch(color=to_rgb(colors[1]), label=round(float(values[1]), 2))
    patch_2 = mpatches.Patch(color=to_rgb(colors[2]), label=round(float(values[2]), 2))
    patch_3 = mpatches.Patch(color=to_rgb(colors[3]), label=round(float(values[3]), 2))
    patch_4 = mpatches.Patch(color=to_rgb(colors[4]), label=round(float(values[4]), 2))
    patch_5 = mpatches.Patch(color=to_rgb(colors[5]), label=round(float(values[5]), 2))
    patch_6 = mpatches.Patch(color=to_rgb(colors[6]), label=round(float(values[6]), 2))
    patch_7 = mpatches.Patch(color=to_rgb(colors[7]), label=round(float(values[7]), 2))
    patch_8 = mpatches.Patch(color=to_rgb(colors[8]), label=round(float(values[8]), 2))
    patch_9 = mpatches.Patch(color=to_rgb(colors[9]), label=round(float(values[9]), 2))

    # legend_tile = "PS (>" + str(acl) + "% ACL)"
    plt.legend(handles=[patch_1, patch_2, patch_3, patch_4, patch_5, patch_6, patch_7, patch_8, patch_9],
               # title=legend_tile,
               loc='center left',
               prop={'size': 6},
               bbox_to_anchor=(1, 0.5))
    plt.setp(ax.get_legend().get_texts(), fontsize='5')  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize='6')  # for legend title

    print("Saving: " + str(out_png_f))

    plt.savefig(out_png_f, dpi=600, bbox_inches='tight')
    plt.clf()


def run():

    try:

        print("8.- Translating blended .tif into .png")
        tif_to_png(input_tif, input_png)

        print("9.- Generating FINAL composite")
        create_visualization(input_png, out_png)

        print("10.- Removing auxiliary files")
        remove_intermediate_files(out_folder)

    except Exception as error:
        print("Error creating the composite visualization {}.".format(error))
        logger.exception('GTiff creation error')
        traceback.print_exc()
    finally:
        print("SUCCESSFULLY created the composite visualization")
        logger.info('Ending composite visualization creation module')
