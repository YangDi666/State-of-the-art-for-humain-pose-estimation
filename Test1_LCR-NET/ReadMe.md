# INRIA - LCR-Net Multi-person 2D and 3D Pose Detection

## Introduction  
- [LCR-NET](https://www.researchgate.net/publication/323510313_LCR-Net_Multi-person_2D_and_3D_Pose_Detection_in_Natural_Images) is realised by INRIA Grenoble team and [here](https://thoth.inrialpes.fr/src/LCR-Net/) are the models.

- Framework:
Pytorch and Detectron

- Methode:
Top-down, humain detection by Mask R-CNN with Detectron + LCR-NET model for key points estimation

- Licence  
 ...

- Database for training:  
Humain3.6M, MPII

#### Advantages 
- A solution for occlusion problem
- Good precision
- 3D and 2D
- 13 joints
- Time : about 340ms/frame common
- Easy installation

## Evaluation 
- Measure the knee angles for each image in the video and create 2 graph to show the variation of the knee angles for the videos and compare the them with the ground truth
- One graph (Results LCR-NET) is created by calculating the angles directly with the algo SK 3D results
- The other (Results Kinect) graph is created by calculating the angles with the 3D claud points constructed from algo SK 2D results by Kinect RGB-D
Tests with Ekinnox's videos  
- Results in Kinect RGB and 3D Cloud points
![ad](https://github.com/YangDi666/State-of-art-for-humain-pose-estimation/blob/master/Test1_LCR-NET/results/Kinect%202d%203d%20and%20skeleton_1.png)
![ad](https://github.com/YangDi666/State-of-art-for-humain-pose-estimation/blob/master/Test1_LCR-NET/results/Kinect%202d%203d%20and%20skeleton_2.png)
![ad](https://github.com/YangDi666/State-of-art-for-humain-pose-estimation/blob/master/Test1_LCR-NET/results/Kinect%202d%203d%20and%20skeleton_3.png)

- Ground truth, Results by LCR-NET 3D and Results by LCR-NET 2D and Kinect Depthmap
![ad](https://github.com/YangDi666/State-of-art-for-humain-pose-estimation/blob/master/Test1_LCR-NET/results/gt_angles.png)
![ad](https://github.com/YangDi666/State-of-art-for-humain-pose-estimation/blob/master/Test1_LCR-NET/results/3dKinect_angles.png)
![ad](https://github.com/YangDi666/State-of-art-for-humain-pose-estimation/blob/master/Test1_LCR-NET/results/3dLcrnet_angles.png)

## Improvement
- Histogramme analysis for depth map to precise the depth value 
![ad](https://github.com/YangDi666/State-of-art-for-humain-pose-estimation/blob/master/Test1_LCR-NET/results/improvement%20for%20the%20graph.png)
![ad](https://github.com/YangDi666/State-of-art-for-humain-pose-estimation/blob/master/Test1_LCR-NET/results/3dKinect_angles%2B.png)

- Trainning with our data
...

## Principle code 
- demo-predict.py 
- demo-show.py
- depth-show.py
- csvWriter.py
- 3Dreconstruction.py
- show_result.py
