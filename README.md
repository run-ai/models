# Run:ai Model Zoo

## Training Models

| Name | Framework | Docker Image |
|-|-|-|
| [Keras Builtin](models/keras/builtin) | Keras + TF | runai/example-tf-keras-builtin |
| [PyTorch Builtin](models/pytorch/builtin) | PyTorch | runai/example-pytorch-builtin |
| [PyTorch Builtin over SSH](models/pytorch/builtin/ssh) | PyTorch | runai/example-pytorch-builtin-ssh |
| [Clara Brain MRI Segmentation](models/clara) | [Clara Train SDK](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/clara-train-sdk) | runai/clara-train-sdk:v3.1.01 |

## Inference Models

| Name | Framework |
|-|-|
| [Marian](models/marian) | [Marian NMT](https://marian-nmt.github.io/) |
| [Triton](models/triton) | [Triton Inference Server](https://developer.nvidia.com/nvidia-triton-inference-server/) |
