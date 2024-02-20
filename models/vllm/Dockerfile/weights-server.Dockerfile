FROM ubuntu:22.04 as builder
ARG ORGANIZATION
ARG MODEL
ARG TOKENIZER_ORGANIZATION=${ORGANIZATION}
ARG TOKENIZER=${MODEL}
ARG SAFETENSORS_ONLY=False

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
RUN python3 download-model.py ${ORGANIZATION}/${MODEL} ${TOKENIZER_ORGANIZATION}/${TOKENIZER} ${SAFETENSORS_ONLY}


FROM vllm/vllm-openai:v0.2.2 as server
ARG MODEL
ENV NAME=${MODEL}
ENV MODEL_NAME_OR_PATH=/model

COPY --from=builder /workdir/${MODEL} /model

EXPOSE 8000
ENTRYPOINT ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server --model ${MODEL_NAME_OR_PATH} --served-model-name ${NAME}"]
