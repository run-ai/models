FROM vllm/vllm-openai:v0.2.2

ARG MODEL
ADD ${MODEL} /model

CMD ["--model", "/model"]
