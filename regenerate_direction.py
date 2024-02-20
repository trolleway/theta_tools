#!/usr/bin/python

import sys
import os
import subprocess




def get_args():
    import argparse
    p = argparse.ArgumentParser(description='Geotag one or more photos with location and orientation from GPX file.')
    p.add_argument('path', help='Path containing JPG files, or location of one JPG file.')

    return p.parse_args()

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


if __name__ == '__main__':
    args = get_args()
    if args.path.lower().endswith(".jpg"):
        # single file
        file_list = [args.path]
    else:

        file_list = []
        for root, sub_folders, files in os.walk(args.path):
            file_list += [os.path.join(root, filename) for filename in files if filename.lower().endswith(".jpg")]



    print("===\nStarting update of {0} images  .\n===".format(len(file_list)))
    
    index = 0
    for filepath in file_list:
        total = len(file_list)
        index = index+1
        if index > total:
            index=total
			
        progress(index, total, status='Add information to '+str(total) + ' photos')
        #command='exiftool -overwrite_original  -P -ProjectionType="equirectangular" -UsePanoramaViewer="True"  -"GPSImgDirection<$exif:GPSImgDirection" -"PoseHeadingDegrees<$exif:GPSImgDirection" -"CroppedAreaImageWidthPixels<$ImageWidth" -"CroppedAreaImageHeightPixels<$ImageHeight" -"FullPanoWidthPixels<$ImageWidth" -"FullPanoHeightPixels<$ImageHeight" -CroppedAreaLeftPixels="0" -CroppedAreaTopPixels="0"  "' + filepath + '"'
        cmd=[]
        cmd.append('exiftool')
        cmd.append('-overwrite_original')
        cmd.append('-P')
        cmd.append('-ProjectionType=equirectangular')
        cmd.append('-UsePanoramaViewer="True"')
        cmd.append('-"GPSImgDirection<$exif:GPSImgDirection"')
        cmd.append('-"PoseHeadingDegrees<$exif:GPSImgDirection"')
        cmd.append('-"CroppedAreaImageWidthPixels<$ImageWidth"')
        cmd.append('-"CroppedAreaImageHeightPixels<$ImageHeight"')
        cmd.append('-"FullPanoWidthPixels<$ImageWidth"')
        cmd.append('-"FullPanoHeightPixels<$ImageHeight"')
        cmd.append('-"CroppedAreaImageWidthPixels<$ImageWidth"')
        cmd.append('-CroppedAreaLeftPixels=0')
        cmd.append('-CroppedAreaTopPixels=0')
        cmd.append(filepath)
        #print command
        subprocess.run(cmd)
    import time
    time.sleep(5)
    
