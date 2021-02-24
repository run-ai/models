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
- `--processes` - The number of launched client processes; default is 5.
- `--requests` - The number of requests to be sent from each process; default is 20.
