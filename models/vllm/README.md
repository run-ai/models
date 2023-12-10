# vLLM Server wrapper

## Overview
vLLM is a fast and easy-to-use library for LLM inference and serving. For more information regarding vLLM look at (https://github.com/vllm-project/vllm).
We wrapped vLLM library and server as a dockerfile ready-to-use and easy to manage with OpenAI API.

## Prerequisite
* Docker
* GPU Machine

## Building the Docker image
There are 2 main targets for build:
* Server (Server only exposed at port 8000)
* App (Includes frontend application exposed at port 3000)

Default target is building the app. For building the server add `--target server` to the following command:
```
docker build --build-arg ORGANIZATION=NousResearch --build-arg MODEL=Llama-2-7b-chat-hf -t run-ai/vllm:Llama-2-7b-chat-hf .
```

## Running the Docker image
Running the application is done with the following command:
```
docker run --rm --gpus all -p 3000:3000 run-ai/vllm:Llama-2-7b-chat-hf
```
To run the server only image change the port to 8000.

## Usage

Using the model for completion example with server image:
```
curl http://localhost:8000/v1/completions -H "Content-Type: application/json" -d '{"model": <MODEL>, "prompt": "Say this is a test", "temperature": 0, "max_tokens": 7}'
```

Using the application with the app image browse to:
```
http://localhost:3000
```
