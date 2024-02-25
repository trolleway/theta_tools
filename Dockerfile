FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn


ARG uid=1000
ARG gid=1000
RUN groupadd -g $gid trolleway && useradd --home /home/trolleway -u $uid -g $gid trolleway  \
  && mkdir -p /home/trolleway && chown -R trolleway:trolleway /home/trolleway
RUN echo 'trolleway:user' | chpasswd


RUN apt-get update && apt-get install --no-install-recommends -y python3-pip time  hugin-tools


#install latest exiftool from https://exiftool.org/forum/index.php?topic=11619.0 https://github.com/marco-schmidt/am/blob/c5b7904cdd1629f08caac09e90f0f53a2393ca1b/Dockerfile#L30
RUN set -ex; \
  export DEBIAN_FRONTEND=noninteractive; \
  apt-get install -y  curl; \
  curl --version; \
  perl -v ;\
  mkdir -p /opt/exiftool ;\
  cd /opt/exiftool ;\
  EXIFTOOL_VERSION=`curl -s https://exiftool.org/ver.txt` ;\
  EXIFTOOL_ARCHIVE=Image-ExifTool-${EXIFTOOL_VERSION}.tar.gz ;\
  curl -s -O https://exiftool.org/$EXIFTOOL_ARCHIVE ;\
  CHECKSUM=`curl -s https://exiftool.org/checksums.txt | grep SHA1\(${EXIFTOOL_ARCHIVE} | awk -F'= ' '{print $2}'` ;\
  echo "${CHECKSUM}  ${EXIFTOOL_ARCHIVE}" | /usr/bin/sha1sum -c  - ;\
  tar xzf $EXIFTOOL_ARCHIVE --strip-components=1 ;\
  rm -f $EXIFTOOL_ARCHIVE ;\
  ./exiftool -ver && cd /
ENV PATH="$PATH:/opt/exiftool"

RUN pip3 install pillow pyexiftool

#add to sudoers
RUN apt-get install -y apt-utils
RUN apt-get install -y sudo
RUN adduser trolleway sudo
RUN usermod -aG sudo trolleway



#RUN MKDIR /opt/photos
#RUN MKDIR /opt/photo_tools

COPY . /opt/photo_tools
WORKDIR /opt/photo_tools
