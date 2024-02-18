docker build --build-arg ORGANIZATION=NousResearch --build-arg MODEL=Llama-2-7b-chat-hf --build-arg SAFETENSORS_ONLY=True -t gcr.io/run-ai-demo/quickstart-inference:Llama-2-7b-chat-hf .
docker push gcr.io/run-ai-demo/quickstart-inference:Llama-2-7b-chat-hf
docker rmi gcr.io/run-ai-demo/quickstart-inference:Llama-2-7b-chat-hf

docker build --build-arg ORGANIZATION=NousResearch --build-arg MODEL=Llama-2-13b-chat-hf --build-arg TOKENIZER_ORGANIZATION=NousResearch --build-arg TOKENIZER=Llama-2-7b-chat-hf --build-arg SAFETENSORS_ONLY=True -t gcr.io/run-ai-demo/quickstart-inference:Llama-2-13b-chat-hf .
docker push gcr.io/run-ai-demo/quickstart-inference:Llama-2-13b-chat-hf
docker rmi gcr.io/run-ai-demo/quickstart-inference:Llama-2-13b-chat-hf

docker build --build-arg ORGANIZATION=tiiuae --build-arg MODEL=falcon-7b-instruct -t gcr.io/run-ai-demo/quickstart-inference:falcon-7b-instruct .
docker push gcr.io/run-ai-demo/quickstart-inference:falcon-7b-instruct
docker rmi gcr.io/run-ai-demo/quickstart-inference:falcon-7b-instruct

docker build --build-arg ORGANIZATION=tiiuae --build-arg MODEL=falcon-40b-instruct -t gcr.io/run-ai-demo/quickstart-inference:falcon-40b-instruct .
docker push gcr.io/run-ai-demo/quickstart-inference:falcon-40b-instruct
docker push gcr.io/run-ai-demo/quickstart-inference:falcon-40b-instruct
