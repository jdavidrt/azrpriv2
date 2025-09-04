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
    conda create -n testbed python=3.9 pytest -y && \
    conda activate testbed && \
    python -m pip install pytest pytest-cov pytest-django pytest-asyncio black isort flake8 mypy django-stubs mkdocs mkdocs-material markdown-include"

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