# This Dockerfile is used to generate the docker image dsarchive/histomicstk
# This docker image includes the HistomicsTK python package along with its
# dependencies.
#
# All plugins of HistomicsTK should derive from this docker image


# start from nvidia/cuda 10.0
# FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04# FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
FROM tensorflow/tensorflow:1.15.4-gpu-py3
LABEL com.nvidia.volumes.needed="nvidia_driver"

LABEL maintainer="Ujwala Guttikonda - Sarder Lab. <ujwalaguttikonda@ufl.edu>"

CMD echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! STARTING THE BUILD !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# RUN mkdir /usr/local/nvidia && ln -s /usr/local/cuda-10.0/compat /usr/local/nvidia/lib

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list

RUN apt-get update && \
    apt-get install --yes --no-install-recommends software-properties-common && \
    # As of 2018-04-16 this repo has the latest release of Python 2.7 (2.7.14) \
    # add-apt-repository ppa:jonathonf/python-2.7 && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get --yes --no-install-recommends -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    git \
    wget \
    python-qt4 \
    python3-pyqt4 \
    curl \
    ca-certificates \
    libcurl4-openssl-dev \
    libexpat1-dev \
    unzip \
    libhdf5-dev \
    libpython-dev \
    libpython3-dev \
    python2.7-dev \
    python-tk \
    python3.6-dev \
    python3.6-distutils \
    python3-tk \
    software-properties-common \
    libssl-dev \   
    build-essential \
    cmake \
    autoconf \
    automake \
    libtool \
    pkg-config \ 
    \
    # useful later \
    libmemcached-dev && \
    \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CHECKPOINT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

RUN apt-get update ##[edited]
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y


WORKDIR /
# Make Python3 the default and install pip.  Whichever is done last determines
# the default python version for pip.
RUN rm /usr/bin/python && \
    ln /usr/bin/python3 /usr/bin/python
RUN curl https://bootstrap.pypa.io/pip/2.6/get-pip.py -O && \
    python2 get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

ENV build_path=$PWD/build

# HistomicsTK sepcific

# copy HistomicsTK files
ENV htk_path=$PWD/HistomicsTK
RUN mkdir -p $htk_path

RUN apt-get update && \
    apt-get install -y --no-install-recommends memcached && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY . $htk_path/
WORKDIR $htk_path

# Install HistomicsTK and its dependencies
#   Upgrade setuptools, as the version in Conda won't upgrade cleanly unless it
# is ignored.
RUN pip install --no-cache-dir --upgrade --ignore-installed pip setuptools && \
    # Install bokeh to help debug dask
    pip install --no-cache-dir 'bokeh>=0.12.14' && \
    # Install large_image memcached extras
    pip install --no-cache-dir --pre 'large-image[memcached]' --find-links https://girder.github.io/large_image_wheels && \
    # Install girder-client
    pip install --no-cache-dir girder-client && \
    # Install HistomicsTK
    pip install --no-cache-dir --pre . --find-links https://girder.github.io/large_image_wheels && \
    # Install GPU version of tensorflow
    # pip install --no-cache-dir 'tensorflow-gpu==1.14.0' && \
    # Install tf-slim
    pip install --no-cache-dir 'tf-slim>=1.1.0' && \
    # Install pillow_lut
    pip install --no-cache-dir 'pillow-lut' && \
    # Install openpyxl
    pip install --no-cache-dir 'openpyxl' && \
    pip install --no-cache-dir 'xlrd==1.2.0' && \
    # Install umap
    pip install --no-cache-dir umap-learn && \
    # Install visdom
    pip install --no-cache-dir 'visdom>=0.1.8.8' && \
    # clean up
    rm -rf /root/.cache/pip/*

# Show what was installed
RUN pip freeze


# define entrypoint through which all CLIs can be run
WORKDIR $htk_path/histomicstk/cli

# Test our entrypoint.  If we have incompatible versions of numpy and
# openslide, one of these will fail
RUN python -m slicer_cli_web.cli_list_entrypoint --list_cli
RUN python -m slicer_cli_web.cli_list_entrypoint PodoSighter_cnn --help

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
