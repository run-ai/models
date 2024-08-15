FROM nvcr.io/nvidia/tritonserver:24.07-py3-sdk

ENTRYPOINT ["perf_analyzer", "-m", "inception_graphdef", "-b", "10", "--percentile=95", "--concurrency-range", "1:4"]
