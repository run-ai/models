FROM nvidia/cuda:10.0-runtime-ubuntu18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        libcudnn7=7.6.0.64-1+cuda10.0 \
        python3.6 \
        curl

RUN apt-get install -y python3.6-distutils
RUN ln -s /usr/bin/python3.6 /usr/bin/python

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

RUN pip install numpy \
        tensorflow-gpu==1.14.0 \
        keras==2.2.4 \
        scipy==1.2.0 \
        pillow

RUN mkdir /workload

COPY ./main.py /workload/
COPY ./cifar-10 /workload/cifar-10

WORKDIR /workload
ENTRYPOINT ["python", "main.py"]
