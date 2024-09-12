# Triton Inference Server

## How To Run

Run the server:
```
docker run -it --rm --gpus all -p 8000:8000 runai.jfrog.io/demo/example-triton-server
```

Run the client:
```
docker run -it --rm --network=host runai.jfrog.io/demo/example-triton-client
```
