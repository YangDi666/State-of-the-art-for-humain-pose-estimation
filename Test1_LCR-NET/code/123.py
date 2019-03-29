
import sys, os, pdb, json
import numpy as np
import pickle
from PIL import Image
import cv2
import scene
import matplotlib.pylab as plt

from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import math
def angle(p1,p2,p3):
    n=len(p1)
    # vectors
    v1=[(p1[i]-p2[i]) for i in range(n)]
    v2=[(p3[i]-p2[i]) for i in range(n)]
    # angle = acos( dot(v1,v2) / (len(v1)*len(v2)) )
    dot=sum([(v1[i]*v2[i]) for i in range(n)])
    len_v1=math.sqrt(sum([(v1[i]**2) for i in range(n)]))
    len_v2=math.sqrt(sum([(v2[i]**2) for i in range(n)]))
    if(len_v1!=0 and len_v2!=0):
        return math.degrees(math.acos(dot/(len_v1*len_v2)))
    else:
        return '999999!'


def get_pos(det, njts, point):
    return (det['pose3d'][point-1],det['pose3d'][point+njts-1],det['pose3d'][point+2*njts-1])

with open('test1/test1.json') as json_data:
    d = json.load(json_data)

    K = d['K']
    njts = d['njts']
    x=d['frames'][100][0]['pose2d'][0:13]
    y=d['frames'][100][0]['pose2d'][13:26]
    z=d['frames'][100][0]['pose3d'][26:39]
    det=d['frames'][100][0]
fig = plt.figure()
ax3d = fig.add_subplot(235)
ax3d.set_aspect('equal')

ax3d.set_xlabel('X axis', labelpad=-5)
ax3d.set_ylabel('Y axis', labelpad=-5)


ax3d.plot(y,x)
plt.show()

det['angle_left']=angle(get_pos(det,njts,2),get_pos(det,njts,4),get_pos(det,njts,6))
det['angle_right']=angle(get_pos(det,njts,1),get_pos(det,njts,3),get_pos(det,njts,5))
          