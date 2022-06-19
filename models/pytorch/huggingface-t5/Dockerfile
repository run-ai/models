FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime

RUN pip install \
    transformers==4.15.0 \
    accelerate==0.5.1 \
    datasets==1.17.0 \
    sentencepiece==0.1.96 \
    protobuf==3.19.3 \
    sacrebleu==2.0.0 \
    py7zr==0.17.2 \
    torch==1.7.0

COPY model.py /model.py

ENTRYPOINT ["python", "/model.py"]
