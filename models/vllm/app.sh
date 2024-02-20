bash -c "python3 -m vllm.entrypoints.openai.api_server --model ${MODEL_NAME_OR_PATH} --served-model-name ${NAME}" &
bash -i -c "npm run dev --prefix chatbot-ui" &
bash -c "python3 ready.py" &
wait -n
