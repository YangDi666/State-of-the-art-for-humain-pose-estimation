# EPFL VITA lab - PifPaf: Composite Fields for Human Pose Estimation
## introduction
[PifPaf](https://arxiv.org/pdf/1903.06593.pdf) of EPFL VITA lab offers a new bottom-up method of 2D human pose estimation using a Part Intensity Field (PIF) to locate body joints and a Part Association Field (PAF) to associate body joints with each other. This method surpasses the previous methods in low resolution,
 cluttered, or obstructed scenes. Thanks to its new PAF composite field and to its choice of the Laplace loss for regressions integrating a notion of uncertainty.

Framework: Pytorch

Method: Bottom-up
- PIF label (confidence map + regression map) for the location of body joints
- PAF label for the association of the joints of the body to each other.

Dataset: COCO keypoint challenge dataset

Characteristics
- Solution in low resolution, crowded, cluttered or clogged scenes
- 2D
- 17 joints.
- Nvidia GTX1080Ti GPU processing time for our data: about 1.5 FPS
- Easy installation
