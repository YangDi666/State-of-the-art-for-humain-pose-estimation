import cv2
import numpy as np
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import math
import tools
import os
import re
from matplotlib.animation import FuncAnimation 
import sys

'''
def init(): 
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1) 
    return ln,
def update(frame): 
    xdata.append(frame) 
    ydata.append(np.sin(frame)) 
    ln.set_data(xdata, ydata) 
    return ln,
'''

def show_angle3d(nb_video, frames): 
    b='3'
    files=os.listdir('testVideos/test'+nb_video+'/') 
    for i in files:
        if (len(re.findall('.*C\.json', i))!=0):
            filejson=i
        if (len(re.findall('.*D.mp4', i))!=0):
            filedepth=i
        if (len(re.findall('.*C.mp4', i))!=0):
            filecolor=i
    print(filejson)
    print(filedepth)
    print(filecolor)
    fig=plt.figure()
    ax=fig.add_subplot(222, projection='3d')
    ax.set_title('Depth map'+b+'_m front')
    ax2=fig.add_subplot(221)
        
    # fig=plt.figure()
    ax2.set_title('Openpose 2D in Color image_'+b+'m front')

    ax3=fig.add_subplot(223, projection='3d')
    ax3.set_title('Openpose SK 2D in Depth map_'+b+'m front')
   
    v_c=cv2.VideoCapture('testVideos/test'+nb_video+'/'+filecolor)

    with open('testVideos/test'+nb_video+'/'+filejson) as json_data:
        d = json.load(json_data)
    v=cv2.VideoCapture('testVideos/test'+nb_video+'/'+filedepth)

    anglesl=[]
    anglesr=[]

    for t in range(frames[0],frames[1]):
        #print(t)
        v.set(cv2.CAP_PROP_POS_FRAMES, t)
        ret, im=v.read()
        v_c.set(cv2.CAP_PROP_POS_FRAMES, t)
        retc, im_c=v_c.read()

        # médian
        img_m=cv2.medianBlur(im,7)
        font=cv2.FONT_HERSHEY_SIMPLEX

    
        x=[]
        y=[]
        z=[]
        
        # show 3d claud points
        for i in range(600,1000,30):
            for j in range(200,960,60):
                a=tools.RGBto3D((i,j),img_m)
                x.append(a[0])
                y.append(a[1])
                z.append(a[2])
        ax3.scatter(x,z,y, s=1)

        
        for i in range(600,1000,3):
            for j in range(200,960,6):
                a=tools.RGBto3D((i,j),img_m)
                x.append(a[0])
                y.append(a[1])
                z.append(a[2])
        ax.scatter(x,z,y, s=1)
        
        
        # show 3d joints
        if len(d['frames'][t])!=0:
            xjoints=d['frames'][t][0]['pose2d'][:18]
            yjoints=d['frames'][t][0]['pose2d'][18:]
            xjoints_3d=[]
            yjoints_3d=[]
            zjoints_3d=[]

            for i in range(18):
                joints=tools.RGBto3D((xjoints[i], yjoints[i]), img_m)
                xjoints_3d.append(joints[0])
                yjoints_3d.append(joints[1])
                zjoints_3d.append(joints[2])

        ax.scatter(xjoints_3d, zjoints_3d, yjoints_3d , color='r')
        ax3.scatter(xjoints_3d, zjoints_3d, yjoints_3d , color='r')
        print(xjoints_3d, zjoints_3d, yjoints_3d)
        
        anglesl.append(180-tools.angle((xjoints_3d[11],yjoints_3d[11],zjoints_3d[11]),(xjoints_3d[12],yjoints_3d[12],zjoints_3d[12]),(xjoints_3d[13],yjoints_3d[13],zjoints_3d[13])))
        anglesr.append(180-tools.angle((xjoints_3d[8],yjoints_3d[8],zjoints_3d[8]),(xjoints_3d[9],yjoints_3d[9],zjoints_3d[9]),(xjoints_3d[10],yjoints_3d[10],zjoints_3d[10])))
        #gt=(54.115166+1100, -1168.320923+27124, 484.712952+1100)
        #ax.scatter(gt[0],gt[1],gt[2], color='y')
        print(xjoints_3d[3], zjoints_3d[3], yjoints_3d[3])
        print(anglesl)
        print(anglesr)
        
        # show 3d skelecton
        ax.plot([xjoints_3d[k] for k in [14,16,0,1,8,9,10]], [zjoints_3d[k] for k in [14,16,0,1,8,9,10]], [yjoints_3d[k] for k in [14,16,0,1,8,9,10]], color='#006400' )
        ax.plot([xjoints_3d[k] for k in [15,17,0,1,11,12,13]], [zjoints_3d[k] for k in [15,17,0,1,11,12,13]], [yjoints_3d[k] for k in [15,17,0,1,11,12,13]], color='#006400' )
        ax.plot([xjoints_3d[k] for k in [4,3,2,1,5,6,7]], [zjoints_3d[k] for k in [4,3,2,1,5,6,7]], [yjoints_3d[k] for k in [4,3,2,1,5,6,7]], color='#006400' )
       
        ax3.plot([xjoints_3d[k] for k in [14,16,0,1,8,9,10]], [zjoints_3d[k] for k in [14,16,0,1,8,9,10]], [yjoints_3d[k] for k in [14,16,0,1,8,9,10]], color='#006400' )
        ax3.plot([xjoints_3d[k] for k in [15,17,0,1,11,12,13]], [zjoints_3d[k] for k in [15,17,0,1,11,12,13]], [yjoints_3d[k] for k in [15,17,0,1,11,12,13]], color='#006400' )
        ax3.plot([xjoints_3d[k] for k in [4,3,2,1,5,6,7]], [zjoints_3d[k] for k in [4,3,2,1,5,6,7]], [yjoints_3d[k] for k in [4,3,2,1,5,6,7]], color='#006400' )
       
        # show color image and the joints 
        ax2.imshow(im_c)    
        ax2.plot([xjoints[k] for k in [14,16,0,1,8,9,10]], [yjoints[k] for k in [14,16,0,1,8,9,10]], color='#00FF00' )
        ax2.plot([xjoints[k] for k in [15,17,0,1,11,12,13]], [yjoints[k] for k in [15,17,0,1,11,12,13]], color='#00FF00')
        ax2.plot([xjoints[k] for k in [4,3,2,1,5,6,7]], [yjoints[k] for k in [4,3,2,1,5,6,7]], color='#00FF00')
        
        ax2.scatter(xjoints, yjoints, color='r', s=15)
        
        # show the joints' positions
        for a in [0,1,2,3,8,9,10]:
                ax2.text(xjoints[a]-300, yjoints[a], '(%.1f, %.1f, %.1f)'%(xjoints_3d[a],yjoints_3d[a], zjoints_3d[a]), color='blue')
        for a in [5,6,11,12,13]:
                ax2.text(xjoints[a]+50, yjoints[a], '(%.1f, %.1f, %.1f)'%(xjoints_3d[a],yjoints_3d[a], zjoints_3d[a]), color='orange')
        ax2.text(xjoints[4]-600, yjoints[4], '(%.1f, %.1f, %.1f)'%(xjoints_3d[4],yjoints_3d[4], zjoints_3d[4]), color='blue')
        ax2.text(xjoints[7]+350, yjoints[7], '(%.1f, %.1f, %.1f)'%(xjoints_3d[7],yjoints_3d[7], zjoints_3d[7]), color='blue')
       
        '''
        print(xjoints)
        print(yjoints)
        print(zjoints)
    ax2.scatter(xjoints, zjoints, yjoints, color='r')
    '''    
        
    v.release()
    frames=range(frames[0],frames[1])
    #ax.plot(frames, anglesl)
    #ax2.plot(frames, anglesr)
    plt.show()

#for frame in range(100,150):
frame=int(sys.argv[1])
show_angle3d('1', [frame, frame+1])
sys.exit(1)
