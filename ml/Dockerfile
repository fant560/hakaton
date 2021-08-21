ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:21.06-py3
FROM ${BASE_IMAGE} as nemo-deps
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
    libsndfile1 sox \
    libfreetype6 \
    python-setuptools swig \
    python-dev ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN pip uninstall -y sacrebleu torchtext

WORKDIR /tmp/torchaudio_build
RUN git clone --depth 1 --branch release/0.7 https://github.com/pytorch/audio.git && \
    cd audio && \
    BUILD_SOX=1 python setup.py install && \
    cd .. && rm -r audio


FROM nemo-deps as nemo
RUN conda install -c numba numba=0.53.1
RUN python -m pip install git+https://github.com/NVIDIA/NeMo.git@main#egg=nemo_toolkit[all]


COPY . .

RUN python server.py
