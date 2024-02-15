bash -c "python3 -m vllm.entrypoints.openai.api_server --model /model --served-model-name ${NAME}" &
bash -i -c "npm run dev --prefix chatbot-ui" &
bash -c "python3 ready.py" &
wait -n
