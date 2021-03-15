FROM pytorch/pytorch:1.5-cuda10.1-cudnn7-runtime

RUN mkdir /workload

COPY ./cifar-10-batches-py /workload/cifar-10-batches-py
COPY ./main.py /workload/

WORKDIR /workload
ENTRYPOINT ["python", "main.py"]
