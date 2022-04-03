# -*- coding: utf-8 -*-

import os
import numpy
import shutil
import traceback

import pipeline.settings
from pipeline.code.exceptions import get_module_logger

logger = get_module_logger(__name__)
APP_ROOT = os.path.abspath(os.path.dirname(__file__))

acl = pipeline.settings.ACHIEVED_CONFIDENCE_LEVEL
high_f = pipeline.settings.HIGHEST_FREQUENCY_TO_EVALUATE
low_f = pipeline.settings.LOWEST_FREQUENCY_TO_EVALUATE
nrows = pipeline.settings.NUMBER_OF_FREQUENCIES
nodata = pipeline.settings.NODATA
out_folder = pipeline.settings.OUTPUT_FOLDER
prn_path = pipeline.settings.DATA_FOLDER
prj_template_path = pipeline.settings.PROJECTION_FILE_TEMPLATE
basename = pipeline.settings.RUN_NAME
template_f = pipeline.settings.template_filename
search_term = pipeline.settings.search_expression

f_step = -(high_f/nrows)  # negative sign (-); Graph displays HIGH f top, and LOW f bottom
all_time = []

template = os.path.join(prn_path, template_f)
asc_file = os.path.join(out_folder, basename + ".asc")
proj_file = os.path.join(out_folder, basename + ".prj")


# Make a list of all power spectra files
def list_files(filespath, extension, search):
    my_files = []
    for root, dirs, files in os.walk(filespath):
        for filename in files:
            if (filename[len(filename)-4:len(filename)] == extension) and search in filename:
                ini = os.path.join(root, filename)
                my_files.append(ini)
    return my_files


def process_data(myfiles):

    master_pw = {}

    for elem in myfiles:

        bname = os.path.splitext(os.path.basename(elem))[0]
        bname3 = bname + ".prn"
        bname4 = os.path.join(prn_path, bname3)

        years = []
        with open(bname4, 'r') as f:
            for line in f:
                a, b = line.split()
                years.append(float(a))

        gross = (max(years) - min(years)) / 2
        this_year = round(gross, 5) + round(min(years), 5)

        if this_year:
            all_time.append(this_year)

        file_path_acl = os.path.join(prn_path, bname + ".ACL")
        acl_file = numpy.loadtxt(file_path_acl)
        x_above_acl = []
        for fila in acl_file:
            # i.e. acl=99
            if fila[1] >= acl:
                x_above_acl.append(round(float(fila[0]), 5))

        pw_list = {}

        file_path_lom = os.path.join(prn_path, bname + ".LOM")
        lom = numpy.loadtxt(file_path_lom)
        for fila2 in lom:
            temp = round(float(fila2[0]), 5)
            if round(float(temp), 5) in x_above_acl:
                if temp in pw_list:
                    if float(fila2[1]) > pw_list[temp]:
                        # pw_list contains the power spectra per year
                        pw_list[round(float(fila2[0]), 5)] = float(fila2[1])
                else:

                    pw_list[round(float(fila2[0]), 5)] = float(fila2[1])  # pw_list tiene el power spectra de cada year

        master_pw[str(this_year)] = pw_list  # cada serie tiene sus power spectra caracteristicos

    return master_pw, all_time


def write_asc(asc_f, years, pw):

    with open(asc_f, 'w') as new_file:
        n_cols = "NCOLS " + str(len(years)) + '\n'
        new_file.write(n_cols)

        n_rows = "NROWS " + str(nrows) + '\n'
        new_file.write(n_rows)

        x_center = "XLLCENTER 330000.5\n"
        new_file.write(x_center)

        y_center = "YLLCENTER 339500.5\n"
        new_file.write(y_center)

        cellsize = "CELLSIZE 1\n"
        new_file.write(cellsize)

        nan = "NODATA_VALUE " + str(nodata) + '\n'
        new_file.write(nan)

        for cycle in numpy.arange(high_f, low_f, f_step):
            row = []
            for age in years:
                cycle = round(cycle, 5)
                if cycle in pw[str(age)]:
                    if isinstance(pw[str(age)], dict):
                        for k2, v2 in pw[str(age)].items():
                            if k2 == cycle:
                                row.append(v2)
                else:
                    row.append(nodata)
            # each cycle written
            to_file = ' '.join(map(str, row)) + '\n'
            new_file.write(to_file)


def add_projection(template_file, proj_filename):

    shutil.copyfile(template_file, proj_filename)


# Function to run all script logic
def run():

    try:

        print("1.- Retrieving files")
        myfiles = list_files(prn_path, '.prn', search_term)

        print("2.- Processing the data")
        master_pw, years = process_data(myfiles)

        print("3.- Writing asc file")
        write_asc(asc_file, years, master_pw)

        print("4.- Adding projection (*.prj) to asc file")
        add_projection(prj_template_path, proj_file)

    except Exception as error:
        print("Error creating the ASCII grid file from spectral analysis results: {}.".format(error))
        logger.exception('ASCII grid creation error')
        traceback.print_exc()
    finally:
        print("SUCCESSFULLY created the ASCII grid file from spectral analysis results")
        logger.info('Ending create ASC module')
