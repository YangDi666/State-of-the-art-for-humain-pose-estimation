## Introduction
[OpenPose](https://arxiv.org/pdf/1812.08008.pdf) of CMU presents an effective method for estimating multi-person pose with a competitive performance on several public repositories. It presents the first bottom-up representation of association scores via Part Affinity Fields (PAFs), a set of 2D vector fields encoding the location and orientation of members in the image domain.

Framework: Caffe, Cuda

Method: Bottom-up
- The entire image as entered for a CNN to jointly predict.
- The confidence map for the detection of the joints of the body and PAF for the association of the joints.
- Bipartite matches of joints to the body.

Dataset: MPII human multi-person, COCO keypoint challenge dataset

Characteristics
- More effective when the number of people is large
- 2D
- 18 body joints or 25 joints with feet.
- Nvidia GTX1080Ti GPU processing time for our data: about 1.9 FPS
