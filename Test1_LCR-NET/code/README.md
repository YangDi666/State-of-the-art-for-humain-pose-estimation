# LCRNet Video Processing

Based on https://thoth.inrialpes.fr/src/LCR-Net/

This project separates the original demo into two parts:

- demo-predict.py
- demo-show.py

Demo predict should be executed inside the cluster. It creates from a source (.mp4 video), a .json file with the same name with the 2D and 3D skeleton information.

Demo show should be executed locally. It creates, from the original source (.mp4 video) and the previously generated .json file a new video called {source}_detected.mp4 with the original video annotated with the skeleton in 2D and 3D.

## Cluster installation with Conda

### Log in to cluster

```bash
ssh nef-devel2
```

### Install miniconda and create environment

```bash
# download
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
# install
bash Miniconda3-latest-Linux-x86_64.sh
# create environment
conda create -n lcrnet python=3.6
```

### Download and install  LCR-Net (v2.0)

```bash
# download Detectron.pytorch
git clone https://github.com/roytseng-tw/Detectron.pytorch

# download LCR-Net
git clone https://gitlab.inria.fr/inriatechsophia/lcrnet-videoprocessing

# activate environment
source activate lcrnet

# load modules
module load cuda/9.1
module load cudnn/7.0-cuda-9.1
module load gcc/6.2.0

# install dependencies
conda install pytorch
conda install torchvision
conda install cython
conda install matplotlib
conda install numpy
conda install scipy
conda install opencv
conda install pyyaml
conda install packaging
pip install pycocotools
pip install tensorboardX
pip install tqdm
pip install h5py
```

Detectron.pytorch installation should be done inside a node with a gpu. For this use an interactive job.

```bash
# reserve and enter a node
oarsub -p "gpu='YES' and gpucapability>='5.0'" -l /nodes=1/gpunum=1,walltime=2 -I

# inside the node
cd Detectron.pytorch/lib

# activate environment
source activate lcrnet

# load modules
module load cuda/9.1
module load cudnn/7.0-cuda-9.1
module load gcc/6.2.0

# install
sh make.sh

# create a symbolic link to Detectron.pytorch from lcrnet root

cd ../../lcrnet-videoprocessing
ln -s ../Detectron.pytorch/
```

### Test installation

```bash
# still inside the node
# execute prediction over the test video
python3 demo-predict.py InTheWild-ResNet50 test/testvideo.mp4 0
```
Once the process is finished, you should see the resulting json file with the 2d and 3d poses for each frame of the video, both displayed in the console and saved into the test folder as testvideo.json

## Process videos

### Perform prediction in the cluster

The prediction is done with a pretrained model, downloaded automatically by the script. 

The list of available models are:

- DEMO_ECCV18: model with fast inference time (downscale image, reduce number of classes) that we use for our ECCV'18 demo
- Human3.6-17J-ResNet50: model trained (and evaluated) on Human3.6M dataset to estimate 17 joints
- InTheWild-ResNet50: model trained on real-world (and synthetic) images evaluated on MPII dataset

Downloaded from http://pascal.inrialpes.fr/data2/grogez/LCR-Net/pthmodels/

Check the job.oar file and modify it to point to your working path and conda environment accordingly.

```bash
# copy your video to the cluster
scp -r {source}.mp4 nef-devel2:/home/{user}/lcrnet-videoprocessing/

# log in to cluster
ssh nef-devel2
cd lcrnet-videoprocessing

# submit job
oarsub -S "lcrnet-videoprocessing/job.oar {source}.mp4 {modelname}"

```

After the job is finished you should find the generated {source}.json file in the lcrnet-videoprocessing folder.  Check the log files (OAR*.stdout and OAR*.stderr) for the job progress and error.

### Install lcrnet-videoprocessing locally

To join the videos and the obtained skeleton locally, you will need to download the lcrnet-videoprocessing project and install the demo-show dependencies. No gpu is needed for this step.

Dependencies:
- python=3.6
- numpy
- opencv-python
- matplotlib
- tqdm

### Create the annotated video

```bash
# copy the json file from the cluster
scp -r nef-devel2:/home/{user}/lcrnet-videoprocessing/{source}.json ./

# perform prediction
python3 demo-show.py {source}.mp4
```

The result will be displayed while creating the video, and will finally be saved under the name {source}_detected.mp4
 