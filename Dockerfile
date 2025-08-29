FROM --platform=linux/x86_64 ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update && apt install -y \
    wget \
    git \
    build-essential \
    libffi-dev \
    libtiff-dev \
    python3 \
    python3-pip \
    python-is-python3 \
    jq \
    curl \
    locales \
    locales-all \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Download and install conda
RUN wget 'https://repo.anaconda.com/miniconda/Miniconda3-py311_23.11.0-2-Linux-x86_64.sh' -O miniconda.sh \
    && bash miniconda.sh -b -p /opt/miniconda3
# Add conda to PATH
ENV PATH=/opt/miniconda3/bin:$PATH
# Add conda to shell startup scripts like .bashrc (DO NOT REMOVE THIS)
RUN conda init --all
RUN conda config --append channels conda-forge

RUN adduser --disabled-password --gecos 'dog' nonroot


RUN /bin/bash -c "set -euxo pipefail && \
    source /opt/miniconda3/bin/activate && \
    conda create -n testbed python=3.9 -y && \
    echo 'aiohttp' > $HOME/requirements.txt && \
    echo 'aioresponses' >> $HOME/requirements.txt && \
    echo 'black' >> $HOME/requirements.txt && \
    echo 'callee' >> $HOME/requirements.txt && \
    echo 'click' >> $HOME/requirements.txt && \
    echo 'coverage' >> $HOME/requirements.txt && \
    echo 'cryptography' >> $HOME/requirements.txt && \
    echo 'flake8' >> $HOME/requirements.txt && \
    echo 'isort' >> $HOME/requirements.txt && \
    echo 'mock' >> $HOME/requirements.txt && \
    echo 'pre-commit' >> $HOME/requirements.txt && \
    echo 'pyjwt' >> $HOME/requirements.txt && \
    echo 'pytest' >> $HOME/requirements.txt && \
    echo 'pytest-mock' >> $HOME/requirements.txt && \
    echo 'pyupgrade' >> $HOME/requirements.txt && \
    echo 'requests' >> $HOME/requirements.txt && \
    echo 'Sphinx' >> $HOME/requirements.txt && \
    echo 'sphinx_rtd_theme' >> $HOME/requirements.txt && \
    echo 'sphinx_mdinclude' >> $HOME/requirements.txt && \
    echo 'setuptools>=65.5.1 # not directly required, pinned by Snyk to avoid a vulnerability' >> $HOME/requirements.txt && \
    conda activate testbed && \
    python -m pip install -r $HOME/requirements.txt && \
    rm $HOME/requirements.txt && \
    conda activate testbed && \
    python -m pip install pytest"

WORKDIR /testbed/

# Automatically activate the testbed environment
RUN echo "source /opt/miniconda3/etc/profile.d/conda.sh && conda activate testbed" > /root/.bashrc

# Setup working directory 
RUN mkdir -p /app
# Copy github repo from Local setu to Docker container
COPY . /app 
WORKDIR /app
RUN /bin/bash -c "pip install -e ."

# Set up Conda shell integration
SHELL ["/bin/bash", "-c"]
# Set up automatic activation of the 'testbed' Conda environment
# This appends the activation command to ~/.bashrc for interactive shells
RUN echo "source /opt/miniconda3/etc/profile.d/conda.sh && conda activate testbed" >> ~/.bashrc
ENV PATH=/opt/miniconda3/envs/testbed/bin:$PATH
ENV CONDA_DEFAULT_ENV=testbed

# Optional: Enter the testcase you wanted to execute here or directly use run command to specify the test cases to run
# Ex: CMD ["pytest", "tests/test_example.py"]