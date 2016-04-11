#!/usr/bin/python

import os
import os.path
import time
import sys
import shutil
from datetime import date
import re
from PIL import Image, ExifTags

# Where the files are
source = sys.argv[1].rstrip('/')

# Where you want the files to go
destination = sys.argv[2].rstrip('/')

def is_image(file):
    image_extensions = [".jpg", ".png", ".gif", ".pef", ".rw2", ".tif", ".xcf", ".psd", ".jpeg"]
    for e in image_extensions:
        if file.lower().endswith(e):
            return True
    
    return False

def is_raw_image(file):
    image_extensions = [".pef", ".rw2"]
    for e in image_extensions:
        if file.lower().endswith(e):
            return True
    
    return False

def is_video(file):
    video_extensions = [".mpg", ".mp4", ".mov", ".avi", ".mts", ".3gp"]
    for e in video_extensions:
        if file.lower().endswith(e):
            return True
    
    return False

def get_exif_dict(file):
    try:
        exif = {}
        img = Image.open(file)

        for k, v in img._getexif().iteritems():
            if k in ExifTags.TAGS:
                exif[ExifTags.TAGS[k]] = v
        
        return exif
    except Exception as e:
        print e
        return None

def get_exif_date(file):
    dict = get_exif_dict(file)
    if not dict:
        return None
        
    if 'DateTimeOriginal' in dict:
        parts = dict['DateTimeOriginal'].split(" ")
        return parts[0].split(":")

    return None
    
for root, dirs, files in os.walk(source):
    for file in files:
        file_path = os.path.join(root, file)
        mtime = time.gmtime(os.path.getmtime(file_path))

        # Some files have their timestamp in the name
        # Prefer that over the mtime        
        m = re.search("(IMG_)?(20[0-9]{6})", file)
        if m:
            filedate = m.group(2)
            mtime = date(int(filedate[0:4]), int(filedate[4:6]), int(filedate[6:8])).timetuple()

        if is_image(file):
            type = "Pictures"
            exif_date = get_exif_date(file_path)
            if exif_date:
                try:
                    year = exif_date[0]
                    month = exif_date[1]
                    day = exif_date[2]
                    mtime = date(int(exif_date[0]), int(exif_date[1]), int(exif_date[2])).timetuple()
                except:
                    pass
        elif is_video(file):
            type = "Videos"
        else:
            type = "Other"

        year = time.strftime("%Y", mtime)
        month = time.strftime("%m_%B", mtime)
        day = time.strftime("%d", mtime)            
                
        new_path = "%s/%s/%s/%s/%s" % (destination, type, year, month, file)
        new_folder = os.path.dirname(new_path)
        if not os.path.exists(new_folder):
            print "Creating folder %s" % new_folder
            os.makedirs(new_folder)
        
        # May want to make this optionally a copy
        print "Moving %s to %s" % (file_path, new_path)
        shutil.move(file_path, new_path)
        
        if is_raw_image(file):
            cmd = "ufraw-batch --out-type=jpg --overwrite --lensfun=none %s" % new_path
            print cmd
            os.system(cmd)
            
            raw_folder = "%s/raw" % new_folder
            if not os.path.exists(raw_folder):
                print "Creating folder %s" % raw_folder
                os.makedirs(raw_folder)
            
            print "Moving %s to %s" % (new_path, raw_folder)
            shutil.move(new_path, raw_folder)
            
