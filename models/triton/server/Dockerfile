FROM nvcr.io/nvidia/tritonserver:24.07-py3

RUN cd / && \
    git clone https://github.com/triton-inference-server/server.git triton-inference-server && \
    cd /triton-inference-server/docs/examples && \
    ./fetch_models.sh

# expose the HTTP port
EXPOSE 8000

ENTRYPOINT ["/opt/nvidia/nvidia_entrypoint.sh", "tritonserver", "--model-repository", "/triton-inference-server/docs/examples/model_repository"]
