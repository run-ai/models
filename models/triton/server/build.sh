#!/bin/sh

docker build -t gcr.io/run-ai-demo/example-triton-server  --platform linux/amd64 -f Dockerfile .
