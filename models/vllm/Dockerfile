FROM vllm/vllm-openai:v0.2.2

ARG MODEL
ENV NAME=${MODEL}

ADD ${MODEL} /model

ENTRYPOINT ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server --model /model --served-model-name ${NAME}"]
