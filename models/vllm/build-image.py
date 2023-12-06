import os
import shutil
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer

def download_and_save_model(model_name):
    save_directory = model_name.split('/')[-1]
    
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model.save_pretrained(save_directory)
    tokenizer.save_pretrained(save_directory)
    return save_directory

def build_docker_image(model):
    docker_build_command = f"docker build --build-arg MODEL={model} -t run-ai/vllm:{model} ."
    os.system(docker_build_command)

def delete_model_directory(model_path):
    shutil.rmtree(model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build dokcer image runs vLLM server with specified model cached.")
    parser.add_argument("model_name", type=str, help="Hugging Face model name")

    args = parser.parse_args()
    saved_model_path = download_and_save_model(args.model_name)
    build_docker_image(saved_model_path)
    delete_model_directory(saved_model_path)

