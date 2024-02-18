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

### Server Only
For building the Server only run the following command:
```
docker build \
		-f Dockerfile/weights-server.Dockerfile \
		--build-arg ORGANIZATION=NousResearch \
		--build-arg MODEL=Llama-2-7b-chat-hf \
		-t server .
```

Optional build args:
* `TOKENIZER_ORGANIZATION` + `TOKENIZER` - To use different tokenizer than the model
* `SAFETENSORS_ONLY=True` - Weather to download only safetensors weight only (Reduce image size)

> [!NOTE]
> For building an weightless server use Dockerfile/weightless-server.Dockerfile instead

### Application
For building also the application run the following command after building the server:
```
docker build \
		-f Dockerfile/app.Dockerfile \
		--build-arg MODEL=Llama-2-7b-chat-hf \
		-t run-ai/vllm:Llama-2-7b-chat-hf .
```

## Running the Docker image
Running the application is done with the following command:
```
docker run --rm --gpus all -p 3000:3000 -p 3001:3001 run-ai/vllm:Llama-2-7b-chat-hf
```
To run the server only image change the port to 8000, and dont expose port 3001.

> [!IMPORTANT]
> For weightless image make sure you set `MODEL_NAME_OR_PATH` env var with HF model name or a path mounted to the container using `-v`


If you wish to run the readiness server on different port than 3001, you can specify it with `-e READINESS_PORT=PORT`
## Usage

Using the model for completion example with server image:
```
curl http://localhost:8000/v1/completions -H "Content-Type: application/json" -d '{"model": <MODEL>, "prompt": "Say this is a test", "temperature": 0, "max_tokens": 7}'
```

Using the application with the app image browse to:
```
http://localhost:3000
```

### Readiness
When running the app, you can check the readiness of the application with the following request:
```
curl http://localhost:3001/ready
```
