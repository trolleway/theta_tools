# theta_tools
my ricoh theta tools for mapillary and google street view


## thetacorrector.py
bulk nadir-zenith correction using nona

## regenerate_direction.py 
bulk regenerate GPS Direction tag. Needed after manual coordinates correction in JOSM for accept by Google Street View service. Requires exiftool program.

## Platform

Windows. Should be work in Ubuntu, but not tested yet. Why you use Ubuntu for work with photos?
## Install

git clone

Install Hugin
Install exiftool into script folder or in system path.

Open thetacorrector.py, change hard-coded nona_path var

## Usage 
thetacorrector.py "E:/photos/2016-05-09_velo_center_theta"
