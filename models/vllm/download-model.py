import os
import shutil
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import snapshot_download

def download_and_save_model(model_name, tokenizer_name, exclude_pytorch_weight):
    save_directory = model_name.split('/')[-1]

    exclude_patterns = ["coreml/*"]
    if exclude_pytorch_weight:
        exclude_patterns.append("*.bin")
    snapshot_download(model_name, local_dir=save_directory, local_dir_use_symlinks=False, ignore_patterns=exclude_patterns)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    tokenizer.save_pretrained(save_directory)

def build_docker_image(model):
    docker_build_command = f"docker build --build-arg MODEL={model} -t run-ai/vllm:{model} ."
    os.system(docker_build_command)

def delete_model_directory(model_path):
    shutil.rmtree(model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build dokcer image runs vLLM server with specified model cached.")
    parser.add_argument("model_name", type=str, help="Hugging Face model name")
    parser.add_argument("tokenizer_name", type=str, help="Hugging Face tokenizer name")
    parser.add_argument("safetensors_only", type=str, help="Download only safetensors weights")

    args = parser.parse_args()
    safetensors = False
    if args.safetensors_only == "True":
        safetensors = True
    download_and_save_model(args.model_name, args.tokenizer_name, safetensors)
