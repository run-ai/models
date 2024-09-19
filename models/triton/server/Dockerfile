FROM nvcr.io/nvidia/tritonserver:24.07-py3

RUN cd / && \
    git clone https://github.com/wcarrollrai/server.git triton-inference-server && \
    cd /triton-inference-server/docs/examples && \
    ./fetch_models.sh && \
    chown root:root /triton-inference-server/docs/examples/model_repository/inception_graphdef/1/model.graphdef && \
    chmod 644 /triton-inference-server/docs/examples/model_repository/inception_graphdef/1/model.graphdef

# expose the HTTP port
EXPOSE 8000

ENTRYPOINT ["/opt/nvidia/nvidia_entrypoint.sh", "tritonserver", "--model-repository", "/triton-inference-server/docs/examples/model_repository"]
