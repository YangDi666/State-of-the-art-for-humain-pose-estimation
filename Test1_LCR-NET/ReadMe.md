# INRIA - LCR-NET SK 3D for Humain pose estimation
- 29/03/2019
## Introduction :  
Based on https://thoth.inrialpes.fr/src/LCR-Net/

### Framework  
- Pytorch 
- Detectron
### Methodes  
End-to-Top, humain detection by Mask R-CNN with Detectron + LCR-NET model for key points estimation
### Licence  

### Database for training  
- Coco
- 
### Advantages 
- A solution for occlusion problem
- Good precision
- 3D and 2D
- 13 joints
- Time : about 340ms/frame common
### Installation  
In the fold "code"
## Evaluation : 
- Measure the knee angles for each image in the video and create 2 graph to show the variation of the knee angles for the videos and compare the them with the ground truth
- One graph (Results LCR-NET) is created by calculating the angles directly with the algo SK 3D results
- The other (Results Kinect) graph is created by calculating the angles with the 3D claud points constructed from algo SK 2D results by Kinect RGB-D
### Tests with Ekinnox's videos  
In folder "results"
### Improve 
- Histogramme analysis for depth map to precise the depth value
- Trainning with our data
## Principle code :
- demo-predict.py 
- demo-show.py
- depth-show.py
- csvWriter.py
- 3Dreconstruction.py
- show_result.py
