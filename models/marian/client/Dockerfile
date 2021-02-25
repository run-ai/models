FROM python:3.6.2

# install marian dependencies
RUN pip install websocket_client

# add the files
ADD entrypoint.sh entrypoint.sh
ADD client_example.py client_example.py
ADD input.txt input.txt

ENV PYTHONUNBUFFERED=1

# run the client
ENTRYPOINT ["./entrypoint.sh"]
