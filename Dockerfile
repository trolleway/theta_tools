FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn


ARG uid=1000
ARG gid=1000
RUN groupadd -g $gid trolleway && useradd --home /home/trolleway -u $uid -g $gid trolleway  \
  && mkdir -p /home/trolleway && chown -R trolleway:trolleway /home/trolleway
RUN echo 'trolleway:user' | chpasswd


RUN apt-get update && apt-get install --no-install-recommends -y python3-pip time exiftool
#RUN pip3 install exif iptcinfo3 



#add to sudoers
RUN apt-get install -y apt-utils
RUN apt-get install -y sudo
RUN adduser trolleway sudo
RUN usermod -aG sudo trolleway



#RUN MKDIR /opt/photos
#RUN MKDIR /opt/photo_tools

COPY . /opt/photo_tools
WORKDIR /opt/photo_tools
