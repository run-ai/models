import os
import shutil
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import snapshot_download

def download_and_save_model(model_name, tokenizer_name):
    save_directory = model_name.split('/')[-1]

    snapshot_download(model_name, local_dir=save_directory, ignore_patterns=["*.bin"])
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

    args = parser.parse_args()
    download_and_save_model(args.model_name, args.tokenizer_name)
