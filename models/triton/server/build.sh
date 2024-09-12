#!/bin/sh

docker build -t runai.jfrog.io/demo/example-triton-server  --platform linux/amd64 -f Dockerfile .
