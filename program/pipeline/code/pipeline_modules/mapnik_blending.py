# -*- coding: utf-8 -*-

import os
import sys
import mapnik

template_file = sys.argv[1]  # template_file XML
basename = sys.argv[2]  # basename for output
out_folder = sys.argv[3]  # out_folder
number_pixels_x = sys.argv[4]  # len(asc.all_years)
number_pixels_y = sys.argv[5]  # number of frequencies (settings)

out_file = os.path.join(out_folder, basename + "_blended.tif")
template_dir = os.path.split(os.path.abspath(template_file))[0]
out_xml = os.path.join(template_dir, basename + ".xml")
out_xml = out_xml.replace('\\r\\n', "")
move_xml = os.path.join(out_folder, basename + ".xml")


def read_write_xml(file_xml, out_xml_f):

    file1 = open(file_xml, 'r')
    lines = file1.readlines()
    with open(out_xml_f, 'wb') as f:
        for line in lines:
            if 'template_color.tif' in line:
                print("Before " + line.rstrip('\r\n'))
                color_tif = basename + "_color.tif"
                line = line.replace("template_color.tif", color_tif)
                print("After " + line.rstrip('\r\n'))
            elif 'template_slopeshade.tif' in line:
                print("Before " + line.rstrip('\r\n'))
                slopeshade_tif = basename + "_slopeshade.tif"
                line = line.replace("template_slopeshade.tif", slopeshade_tif)
                print("After " + line.rstrip('\r\n'))
            elif 'template_hill.tif' in line:
                print("Before " + line.rstrip('\r\n'))
                hillshade_tif = basename + "_hillshade.tif"
                line = line.replace("template_hill.tif", hillshade_tif)
                print("After " + line.rstrip('\r\n'))
            else:
                line = line

            f.write(line)
    file1.close()

    os.rename(out_xml, move_xml)


if __name__ == '__main__':

    # these functions work with mapnik in python2
    print("6.- Creating mapnik template")
    read_write_xml(template_file, out_xml)
    program_map = mapnik.Map(int(number_pixels_x), int(number_pixels_y))
    mapnik.load_map(program_map, move_xml)
    program_map.zoom_all()
    print("7.- Creating mapnik file")
    mapnik.render_to_file(program_map, out_file)
