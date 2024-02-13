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

COPY --from=builder /workdir/${MODEL} /model

EXPOSE 8000
ENTRYPOINT ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server --model /model --served-model-name ${NAME}"]


FROM ubuntu:22.04 as app_builder
ARG MODEL
ARG MODEL_MAX_LENGTH=4096
ARG MODEL_TOKEN_LIMIT=2048

RUN apt-get update -y \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workdir
RUN git clone https://github.com/run-ai/chatbot-ui \
    && cd chatbot-ui \
    && git reset --hard 11fb669
RUN rm -rf .git

ADD web_add_model.patch web_add_model.patch
RUN sed -e 's/<MODEL_NAME>/'"${MODEL}"'/g' \
        -e 's/<MODEL_MAX_LENGTH>/'"${MODEL_MAX_LENGTH}"'/g' \
        -e 's/<MODEL_TOKEN_LIMIT>/'"${MODEL_TOKEN_LIMIT}"'/g' \
    web_add_model.patch > ready.patch

RUN patch chatbot-ui/types/openai.ts ready.patch


FROM server as app
ARG MODEL
ENV OPENAI_API_KEY=none
ENV OPENAI_API_HOST=http://localhost:8000
ENV DEFAULT_MODEL=${MODEL}

RUN apt-get update -y \
    && apt-get install -y curl tini \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "--login", "-i", "-c"]
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
RUN source /root/.bashrc && nvm install --lts

COPY --from=app_builder /workdir/chatbot-ui chatbot-ui
RUN npm i --prefix chatbot-ui

EXPOSE 3000
COPY app.sh app.sh
RUN chmod +x app.sh
ENTRYPOINT ["tini", "--", "bash", "-c", "./app.sh"]
