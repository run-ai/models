build:
	docker build \
		-f Dockerfile/server.Dockerfile \
		--build-arg ORGANIZATION=NousResearch \
		--build-arg MODEL=Llama-2-7b-chat-hf \
		--build-arg SAFETENSORS_ONLY=True \
		-t server .

	docker build \
		-f Dockerfile/app.Dockerfile \
		--build-arg MODEL=Llama-2-7b-chat-hf \
		-t gcr.io/run-ai-demo/quickstart-inference:Llama-2-7b-chat-hf .
	docker push gcr.io/run-ai-demo/quickstart-inference:Llama-2-7b-chat-hf
	docker rmi gcr.io/run-ai-demo/quickstart-inference:Llama-2-7b-chat-hf
