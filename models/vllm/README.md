# vLLM Server wrapper

## Overview
vLLM is a fast and easy-to-use library for LLM inference and serving. For more information regarding vLLM look at (https://github.com/vllm-project/vllm).
We wrapped vLLM library and server as a dockerfile ready-to-use and easy to manage.

## Prerequisite
A model repository cloned from HuggingFace, or any other model repository.

## Building the Docker image
```
docker build --build-arg MODEL=<PATH TO MODEL> -t run-ai/vllm:model .
```

## Running the Docker image
```
docker run --rm --gpus all -p 8000:8000 run-ai/vllm:model
```
