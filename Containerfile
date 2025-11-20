FROM debian:trixie as build

RUN apt-get update && \
    apt-get install -y debhelper-compat dh-python python3 blends-dev

WORKDIR /opt/d9

COPY debian/ debian/
COPY tasks/ tasks/

RUN /usr/share/blends-dev/blend-gen-control -r stable -S -c -t

RUN dpkg-buildpackage -us -uc -b
