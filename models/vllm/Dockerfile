FROM ubuntu:22.04 as builder
ARG ORGANIZATION
ARG MODEL

RUN apt-get update -y \
    && apt-get install -y python3 \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workdir
ADD Dockerfile Dockerfile
ADD download-model.py download-model.py
ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN python3 download-model.py ${ORGANIZATION}/${MODEL}


FROM vllm/vllm-openai:v0.2.2
ARG MODEL
ENV NAME=${MODEL}

COPY --from=builder /workdir/${MODEL} /model

EXPOSE 8000
ENTRYPOINT ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server --model /model --served-model-name ${NAME}"]
