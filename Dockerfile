# This Dockerfile is used to generate the docker image dsarchive/histomicstk
# This docker image includes the HistomicsTK python package along with its
# dependencies.
#
# All plugins of HistomicsTK should derive from this docker image

FROM dsarchive/base_docker_image
LABEL maintainer="Kitware, Inc. <kitware@kitware.com>"

FROM nvidia/cuda:10.2-base
CMD nvidia-smi

# copy HistomicsTK files
ENV htk_path=$PWD/HistomicsTK
RUN mkdir -p $htk_path

RUN apt-get update && \
    apt-get install -y --no-install-recommends memcached && \
    apt-get autoremove && \
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
    pip install --no-cache-dir 'tensorflow-gpu==1.14.0' && \
    # Install tf-slim
    pip install --no-cache-dir 'tf-slim>=1.1.0' && \
    # Downgrade gast
    pip install --no-cache-dir 'gast==0.2.2' && \
    # clean up
    rm -rf /root/.cache/pip/*

# Show what was installed
RUN pip freeze

# pregenerate font cache
RUN python -c "from matplotlib import pylab"

# define entrypoint through which all CLIs can be run
WORKDIR $htk_path/histomicstk/cli

# Test our entrypoint.  If we have incompatible versions of numpy and
# openslide, one of these will fail
RUN python -m slicer_cli_web.cli_list_entrypoint --list_cli
RUN python -m slicer_cli_web.cli_list_entrypoint DetectGlomeruli --help

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
