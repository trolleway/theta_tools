#!/usr/bin/python3

import sys
import os
import subprocess


from exiftool import ExifToolHelper


def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret
'''    
def get_exif3(fn):
    #img = PIL.Image.open(fn)

    for (k,v) in Image.open(fn)._getexif().iteritems():
        print('{k} = {v}'.format(k=TAGS.get(k),v=v) )
'''


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

    
def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
        
    return None
    

    
def print_pto(filepath,new_filepath,pitch,roll):
    
    pto=open('temp.pto', 'w')
    line='i w5376 h2688 f4 v360 r'+str(roll)+' p'+str(pitch)+' y0 n"'+filepath+'"'+"\n"
    pto.write(line)    
    line='p w5376 h2688 f2 v360 r0 p0 y0 n"JPEG q97"'
    pto.write(line)
    pto.close()
    
 
def theta_horizont_auto_correction(filepath):
    '''
    
    '''
    nona_path=r'''C:\Program Files\Hugin2015\bin\nona.exe'''
    nona_path = 'nona'
    #get photo data
    with ExifToolHelper() as et:
        metadata = et.get_metadata(filepath)
    try:
        pitch = metadata[0]['XMP:PosePitchDegrees']
        roll = metadata[0]['XMP:PoseRollDegrees']
    except:
        return False        

    directory = os.path.join(os.path.dirname(filepath),'horizont_correction')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    #new_filepath=os.path.join(os.path.dirname(filepath),os.path.splitext(os.path.basename(filepath))[0]+'_hor'+'.jpg')
    new_filepath=os.path.join(directory,os.path.splitext(os.path.basename(filepath))[0]+'_hor'+'.jpg')
    print_pto(filepath,new_filepath,pitch,roll)
    run_str='"'+nona_path+'" -o "'+new_filepath+'"    temp.pto'
    cmd=[nona_path,'-o',new_filepath,'temp.pto']
    print(cmd)
    subprocess.run(cmd)
    #-tagsFromFile source_image.jpg -XMP:All= -ThumbnailImage= -m destination_image.jpg
    

    s_params=' -tagsFromFile "%s"' % filepath+' -overwrite_original -XMP:PosePitchDegrees=0 -XMP:PoseRollDegrees=0 -quiet -ThumbnailImage= -m "%s"' % new_filepath
    cmd = 'exiftool '+s_params
    os.system(cmd)

        



if __name__ == '__main__':
    args = get_args()
    if args.path.lower().endswith(".jpg"):
        # single file
        file_list = [args.path]
    else:

        file_list = []
        for root, sub_folders, files in os.walk(args.path):
            file_list += [os.path.join(root, filename) for filename in files if filename.lower().endswith(".jpg") and 'horizont_correction' not in os.path.join(root, filename)]



    print("===\nStarting update of {0} images  .\n===".format(len(file_list)))
    
    index = 0
    for filepath in file_list:
        total = len(file_list)
        index = index+1
        if index > total:
            index=total
        progress(index, total, status='Add information to '+str(total) + ' photos')
        theta_horizont_auto_correction(filepath)
        
    
