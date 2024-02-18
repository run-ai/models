DOCKER := docker
BASE_IMAGE := gcr.io/run-ai-demo/quickstart-inference
INTERMEDIATE_IMAGE := server
SERVER_DOCKERFILE ?= Dockerfile/server.Dockerfile
APP_DOCKERFILE ?= Dockerfile/app.Dockerfile

Llama-2-7b-chat-hf:
        $(DOCKER) build \
                -f $(SERVER_DOCKERFILE) \
                --build-arg ORGANIZATION=NousResearch \
                --build-arg MODEL=Llama-2-7b-chat-hf \
                --build-arg SAFETENSORS_ONLY=True \
                -t $(INTERMEDIATE_IMAGE) .

        $(DOCKER) build \
                -f $(APP_DOCKERFILE) \
                --build-arg MODEL=Llama-2-7b-chat-hf \
                -t $(BASE_IMAGE):Llama-2-7b-chat-hf .
        $(DOCKER) push $(BASE_IMAGE):Llama-2-7b-chat-hf
        $(DOCKER) rmi $(BASE_IMAGE):Llama-2-7b-chat-hf $(INTERMEDIATE_IMAGE)

Llama-2-13b-chat-hf:
        $(DOCKER) build \
                -f $(SERVER_DOCKERFILE) \
                --build-arg ORGANIZATION=NousResearch \
                --build-arg MODEL=Llama-2-13b-chat-hf \
                --build-arg TOKENIZER_ORGANIZATION=NousResearch \
                --build-arg TOKENIZER=Llama-2-7b-chat-hf \
                --build-arg SAFETENSORS_ONLY=True \
                -t $(INTERMEDIATE_IMAGE) .

        $(DOCKER) build \
                -f $(APP_DOCKERFILE) \
                --build-arg MODEL=Llama-2-13b-chat-hf \
                -t $(BASE_IMAGE):Llama-2-13b-chat-hf .
        $(DOCKER) push $(BASE_IMAGE):Llama-2-13b-chat-hf
        $(DOCKER) rmi $(BASE_IMAGE):Llama-2-13b-chat-hf $(INTERMEDIATE_IMAGE)

falcon-7b-instruct:
        $(DOCKER) build \
                -f $(SERVER_DOCKERFILE) \
                --build-arg ORGANIZATION=tiiuae \
				--build-arg MODEL=falcon-7b-instruct \
                -t $(INTERMEDIATE_IMAGE) .

        $(DOCKER) build \
                -f $(APP_DOCKERFILE) \
                --build-arg MODEL=falcon-7b-instruct \
                -t $(BASE_IMAGE):falcon-7b-instruct .
        $(DOCKER) push $(BASE_IMAGE):falcon-7b-instruct
        $(DOCKER) rmi $(BASE_IMAGE):falcon-7b-instruct $(INTERMEDIATE_IMAGE)

falcon-40b-instruct:
        $(DOCKER) build \
                -f $(SERVER_DOCKERFILE) \
                --build-arg ORGANIZATION=tiiuae \
				--build-arg MODEL=falcon-40b-instruct \
                -t $(INTERMEDIATE_IMAGE) .

        $(DOCKER) build \
                -f $(APP_DOCKERFILE) \
                --build-arg MODEL=falcon-40b-instruct \
                -t $(BASE_IMAGE):falcon-40b-instruct .
        $(DOCKER) push $(BASE_IMAGE):falcon-40b-instruct
        $(DOCKER) rmi $(BASE_IMAGE):falcon-40b-instruct $(INTERMEDIATE_IMAGE)

all: Llama-2-7b-chat-hf Llama-2-13b-chat-hf falcon-7b-instruct falcon-40b-instruct
