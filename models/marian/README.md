# Marian

## How To Run

Run the server:
```
docker run -it --rm -p 8888:8888 runai/example-marian-server
```

Run the client:
```
docker run -it --rm --network=host runai/example-marian-client
```

You can pass the following arguments:
- `--hostname` - Configure the IP of the server; default is `localhost`.
- `--port` - Configure the port of the server; default is 8888.
- `--processes` - The number of launched client processes; can be multiple values; default is 5.
- `--requests` - The number of requests to be sent from each process; can be multiple values; default is 20.
- `--sentences` - The number of sentences to be translated in each request; can be multiple values; default is 5.
- `--connect-per` (options: `process`, `request`) - Create a socket once per process or for every request; default is `request`.
- `--verbose` - Print verbose messages.
