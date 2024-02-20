FROM vllm/vllm-openai:v0.2.2 as server
ARG MODEL
ARG ORGANIZATION
ENV NAME=${MODEL}
ENV MODEL_NAME_OR_PATH=${ORGANIZATION}/${MODEL}

EXPOSE 8000
ENTRYPOINT ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server --model ${MODEL_NAME_OR_PATH} --served-model-name ${NAME}"]
