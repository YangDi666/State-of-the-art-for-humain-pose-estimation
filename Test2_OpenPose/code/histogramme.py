import cv2
import matplotlib.pylab as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import json 
import tools
import os
import re
from matplotlib.animation import FuncAnimation 

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

    files=os.listdir('testVedios/test'+nb_video+'/') 
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
    ax=fig.add_subplot(121, projection='3d')
    ax.set_title('3D claud points')
    ax2=fig.add_subplot(122)
        
    # fig=plt.figure()
    ax2.set_title('2D color image')
    v_c=cv2.VideoCapture('testVedios/test'+nb_video+'/'+filecolor)

    with open('testVedios/test'+nb_video+'/'+filejson) as json_data:
        d = json.load(json_data)
    v=cv2.VideoCapture('testVedios/test'+nb_video+'/'+filedepth)

    anglesl=[]
    anglesr=[]

    for t in range(frames[0],frames[1]):
        #print(t)
        v.set(cv2.CAP_PROP_POS_FRAMES, t)
        ret, im=v.read()
        v_c.set(cv2.CAP_PROP_POS_FRAMES, t)
        retc, im_c=v_c.read()

        # médian
        img_m=cv2.medianBlur(im,5)
        font=cv2.FONT_HERSHEY_SIMPLEX
        
        x=[]
        y=[]
        z=[]
        
        # show 3d claud points
        for i in range(600,1000,3):
            for j in range(200,960,6):
                a=tools.RGBto3D((i,j),img_m)
                x.append(a[0])
                y.append(a[1])
                z.append(a[2])
        ax.scatter(x,z,y, s=1)
        
        # show 3d joints
        if len(d['frames'][t])!=0:
            xjoints=d['frames'][t][0]['pose2d'][:13]
            yjoints=d['frames'][t][0]['pose2d'][13:]
            xjoints_3d=[]
            yjoints_3d=[]
            zjoints_3d=[]

            for i in range(13):
                joints=tools.RGBto3D((xjoints[i], yjoints[i]), img_m)
                xjoints_3d.append(joints[0])
                yjoints_3d.append(joints[1])
                zjoints_3d.append(joints[2])

        ax.scatter(xjoints_3d, zjoints_3d, yjoints_3d , color='r')
        '''
        anglesl.append(180-tools.angle((xjoints_3d[1],yjoints_3d[1],zjoints_3d[1]),(xjoints_3d[3],yjoints_3d[3],zjoints_3d[3]),(xjoints_3d[5],yjoints_3d[5],zjoints_3d[5])))
        anglesr.append(180-tools.angle((xjoints_3d[0],yjoints_3d[0],zjoints_3d[0]),(xjoints_3d[2],yjoints_3d[2],zjoints_3d[2]),(xjoints_3d[4],yjoints_3d[4],zjoints_3d[4])))
        gt=(54.115166+1100, -1168.320923+27124, 484.712952+1100)
        #ax.scatter(gt[0],gt[1],gt[2], color='y')
        print(xjoints_3d[3], zjoints_3d[3], yjoints_3d[3])
        print(anglesl)
        print(anglesr)
        '''
        # show 3d skelecton
        ax.plot([xjoints_3d[k] for k in [0,2,4,5,3,1]], [zjoints_3d[k] for k in [0,2,4,5,3,1]], [yjoints_3d[k] for k in [0,2,4,5,3,1]], color='orange' )
        ax.plot([xjoints_3d[k] for k in [6,8,10,11,9,7]], [zjoints_3d[k] for k in [6,8,10,11,9,7]], [yjoints_3d[k] for k in [6,8,10,11,9,7]], color='orange' )
        ax.plot([xjoints_3d[12] , (xjoints_3d[4]+xjoints_3d[5])/2], [zjoints_3d[12], (zjoints_3d[4]+zjoints_3d[5])/2], [yjoints_3d[12], (yjoints_3d[4]+yjoints_3d[5])/2], color='orange' )
        
        # show color image and the joints 
        ax2.imshow(im_c)    
        ax2.plot([xjoints[k] for k in [0,2,4,5,3,1]], [yjoints[k] for k in [0,2,4,5,3,1]] )
        ax2.plot([xjoints[k] for k in [6,8,10,11,9,7]], [yjoints[k] for k in [6,8,10,11,9,7]])
        ax2.plot([xjoints[12] , (xjoints[4]+xjoints[5])/2], [yjoints[12], (yjoints[4]+yjoints[5])/2])
        ax2.scatter(xjoints, yjoints, color='r', s=5)
        
        # show the joints' positions
        for a in range(0, 12, 2):
                ax2.text(xjoints[a]-500, yjoints[a], '(%.1f, %.1f, %.1f)'%(xjoints_3d[a],yjoints_3d[a], zjoints_3d[a]), color='blue')
        for a in range(1, 13, 2):
                ax2.text(xjoints[a]+50, yjoints[a], '(%.1f, %.1f, %.1f)'%(xjoints_3d[a],yjoints_3d[a], zjoints_3d[a]), color='orange')
        ax2.text(xjoints[12]-10, yjoints[12]-10, '(%.1f, %.1f, %.1f)'%(xjoints_3d[12],yjoints_3d[12], zjoints_3d[12]), color='g')
   
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
frame=180
show_angle3d('1', [frame, frame+1])
