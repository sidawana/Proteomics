FROM python:3.8-slim-buster


COPY . /app
WORKDIR /app

RUN apt-get update 
RUN apt-get install -y wget 
RUN  apt-get clean  
RUN  rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR /opt/conda

ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

ENV PATH=$CONDA_DIR/bin:$PATH

RUN conda install -c salilab dssp --yes
RUN conda install -c conda-forge biopython
RUN conda install  pandas
RUN pip install pyarrow

