FROM nvidia/cuda:10.1-devel-ubuntu18.04

# install marian dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    build-essential \
    libboost-all-dev \
    libprotobuf10 \
    protobuf-compiler \
    libprotobuf-dev \
    openssl \
    libssl-dev \
    libgoogle-perftools-dev \
&& rm -rf /var/lib/apt/lists/*

# download cmake 3.12.2; the default version for this distribution causes errors
RUN wget https://cmake.org/files/v3.12/cmake-3.12.2.tar.gz && tar -xzf cmake-3.12.2.tar.gz

# install cmake from source
RUN cd cmake-3.12.2 && ./bootstrap && make -j$(nproc) && make install

# clone marian
RUN git clone https://github.com/marian-nmt/marian

# build marian and marian-server
RUN mkdir marian/build && cd marian/build && cmake -DCOMPILE_SERVER=ON .. && make -j4

# link built marian to /build
RUN ln -s /marian/build /build

# clone marian examples
RUN git clone https://github.com/marian-nmt/marian-examples.git

# download tools
RUN cd /marian-examples/tools && make all

# set the working directory
WORKDIR /marian-examples/training-basics

# download files
RUN ./scripts/download-files.sh

# hotpatch a bug in preprocessing the data
RUN mkdir model

# preprocess the data
RUN ./scripts/preprocess-data.sh

# modify runme.sh
RUN \
    sed -i 's/$MARIAN_TRAIN/$MARIAN_TRAIN --after-batches 101/g' run-me.sh && \
    sed -i 's/--save-freq 10000/--save-freq 100/g' run-me.sh && \
    sed -i 's/# translate dev set/exit 0/g' run-me.sh

# train the model
RUN ./run-me.sh

# expose port 8888
EXPOSE 8888

# run the server
ENTRYPOINT ["/marian/build/marian-server", "--port", "8888", "-m", "model/model.npz", "-v", "model/vocab.en.yml", "-v", "model/vocab.ro.yml", "--mini-batch", "5"]
