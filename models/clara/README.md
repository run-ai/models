# Clara

This is a walktrhough guide of how to run the [Clara Brain MRI Segmentation](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/med/models/clara_pt_brain_mri_segmentation) model.

## Test Environments
* 1 GCP machine with 2 Tesla T4 GPUs
* 2 EC2 `g4dn.xlarge` machines each with 1 Tesla T4 GPU

## Setup
Do the following on all your machines including GPU nodes as well as CPU nodes.

### Prerequisites
```
sudo apt install -y unzip
```

### Workspace
```
mkdir -p ~/clara
cd ~/clara
```

### Download Model
```
mkdir model
cd model
wget --content-disposition https://api.ngc.nvidia.com/v2/models/nvidia/med/clara_mri_seg_brain_tumors_br16_full_amp/versions/1/zip -O clara_mri_seg_brain_tumors_br16_full_amp_1.zip
unzip clara_mri_seg_brain_tumors_br16_full_amp_1.zip
chmod +x commands/*.sh
cd ..
```

### Download Data
```
mkdir data
cd data
wget https://www.cbica.upenn.edu/sbia/Spyridon.Bakas/MICCAI_BraTS/2018/MICCAI_BraTS_2018_Data_Training.zip -O MICCAI_BraTS_2018_Data_Training.zip
unzip MICCAI_BraTS_2018_Data_Training.zip
cd ..
```

## Run
After setting up all the above, the Clara model and data should be available on all nodes.

You can run it with Docker commands or with the Run.ai CLI.

> NOTE: The commands here assume that the username is `ubuntu`

### Docker
```
sudo docker run -it --rm --gpus all -v ~/clara/model:/clara -w /clara -v ~/clara/data:/workspace/data/brats2018challenge/training --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 nvcr.io/nvidia/clara-train-sdk:v3.1.01
cd commands/
```

Then train using one of the commands `./train.sh` or `./train_2gpu.sh` depending on how many GPUs you have on the machine.

### Submit Run.ai Job
```
runai submit -g 2 -i nvcr.io/nvidia/clara-train-sdk:v3.1.01 -v /home/ubuntu/clara/model:/clara --working-dir /clara/commands -v /home/ubuntu/clara/data:/workspace/data/brats2018challenge/training --command -- bash -c \"./train_2gpu.sh\"
```

## Run with MPI
### Build Docker Image
We need to make a few modifications in order to run the training with MPI:
1. Install SSH client and server
2. Remove the argument `-H localhost:2` from the `mpirun` command in `train_2gpu.sh`
3. Add the argument `-x PYTHONPATH` to the `mpirun` command in `train_2gpu.sh`

[Here](https://github.com/kubeflow/mpi-operator/blob/3f808b1c592c767b8d4b60613cad385c7a81dee0/build/base/Dockerfile) is an example Dockerfile by the MPI Operator that we based on in our [Dockekrfile](./clara.Dockerfile).

Copy [clara.Dockekrfile](./clara.Dockerfile) to your machines and build the Docker image using the command:

```
sudo docker build -f clara.Dockerfile -t runai/clara-train-sdk:v3.1.01 .
```

### Submit Run.ai MPI Job
```
runai submit-mpi --processes 2 -g 1 -i runai/clara-train-sdk:v3.1.01 --image-pull-policy Never -v /home/ubuntu/clara/model:/clara --working-dir /clara/commands -v /home/ubuntu/clara/data:/workspace/data/brats2018challenge/training
```
