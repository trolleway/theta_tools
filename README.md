# theta_tools
my ricoh theta tools for mapillary and google street view


## thetacorrector.py
bulk nadir-zenith correction using nona

## regenerate_direction.py 
bulk regenerate GPS Direction tag. Needed after manual coordinates correction in JOSM for accept by Google Street View service. Requires exiftool program.

## Platform

Windows. Should be work in Ubuntu, but not tested yet. Why you use Ubuntu for work with photos?
## Install
```
git clone https://github.com/trolleway/theta_tools.git
```
Install Hugin
Install exiftool into script folder or in system path.

Open thetacorrector.py, change hard-coded nona_path var

## Usage 

1. Refrence photo coordinates to GPX tracks using JOSM with his modules or GeoSetter with latest version ExifTool. I prefer JOSM, it more quickly interface.

2. 
```
regenerate_direction.py "E:/photos/2016-05-09_velo_center_theta"

thetacorrector.py "E:/photos/2016-05-09_velo_center_theta"
```


## Create Send To entries in Windows
Assuming Windows 7, If you open a folder and type "shell:sendto" in the address bar then hit enter you'll be taken to the context menu. You can add a .cmd file with the following in it.
```
@echo off
cls
python C:\Your\File\uploadscript.py %1
```
