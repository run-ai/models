# vLLM Server wrapper

## Overview
vLLM is a fast and easy-to-use library for LLM inference and serving. For more information regarding vLLM look at (https://github.com/vllm-project/vllm).
We wrapped vLLM library and server as a dockerfile ready-to-use and easy to manage with OpenAI API.

## Prerequisite
* Docker
* GPU Machine

## Building the Docker image
```
docker build --build-arg ORGANIZATION=NousResearch --build-arg MODEL=Llama-2-7b-chat-hf -t run-ai/vllm:Llama-2-7b-chat-hf .
```

## Running the Docker image
```
docker run --rm --gpus all -p 8000:8000 run-ai/vllm:Llama-2-7b-chat-hf
```

## Usage

Using the model for completion example:
```
curl http://localhost:8000/v1/completions -H "Content-Type: application/json" -d '{"model": <MODEL>, "prompt": "Say this is a test", "temperature": 0, "max_tokens": 7}'
```
