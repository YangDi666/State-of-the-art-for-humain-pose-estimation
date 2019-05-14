

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
    b=str(frames[0])
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
    fig2=plt.figure()
    fig3=plt.figure()
    def call_back(event):
        axtemp=event.inaxes
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        z_min, z_max = axtemp.get_zlim()
        dx = (x_max - x_min) / 10
        dy = (y_max - y_min) / 10
        dz = (z_max - z_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + dx, x_max - dx))
            axtemp.set(ylim=(y_min + dy, y_max - dy))
            axtemp.set(zlim=(z_min + dz, z_max - dz))
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - dx, x_max + dx))
            axtemp.set(ylim=(y_min - dy, y_max + dy))
            axtemp.set(zlim=(z_min - dz, z_max + dz))
 
        fig2.canvas.draw_idle()  # 绘图动作实时反映在图像上
    fig2.canvas.mpl_connect('scroll_event', call_back)
    fig2.canvas.mpl_connect('button_press_event', call_back)
    
    # Depthmap
    ax=fig2.add_subplot(111, projection='3d')
    ax.set_title('PifPaf 2D to Kinect 3D_'+b)

    # Color Image 
    ax2=fig.add_subplot(111)     
    # fig=plt.figure()
    ax2.set_title('PifPaf 2D in Color image_'+b)
    ax5=fig3.add_subplot(111)
    ax5.set_title('PifPaf 2D in Depth image_'+b)
    # sk2d in depthmap
    #ax4=fig.add_subplot(223, projection='3d')
    #ax4.set_title('LCR-NET SK 2D in Depth map_'+b+'m front')


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
        
        if len(d['frames'][t])!=0:
            #SK 2D
            xjoints=d['frames'][t][0]['pose2d'][:17]
            yjoints=d['frames'][t][0]['pose2d'][17:]

            #SK 2D in Depth
            xjoints_3d=[]
            yjoints_3d=[]
            zjoints_3d=[]

            for i in range(17):
                
                joints=tools.RGBto3D((xjoints[i], yjoints[i]), img_m, True, 7)
                xjoints_3d.append(joints[0])
                yjoints_3d.append(joints[1])
                zjoints_3d.append(joints[2])

            print(xjoints_3d, yjoints_3d, zjoints_3d)
        # show joints
        ax.scatter(xjoints_3d, zjoints_3d, yjoints_3d , color='r')
        #ax4.scatter(xjoints_3d, zjoints_3d, yjoints_3d , color='r')
        '''
        anglesl.append(180-tools.angle((xjoints_3d[1],yjoints_3d[1],zjoints_3d[1]),(xjoints_3d[3],yjoints_3d[3],zjoints_3d[3]),(xjoints_3d[5],yjoints_3d[5],zjoints_3d[5])))
        anglesr.append(180-tools.angle((xjoints_3d[0],yjoints_3d[0],zjoints_3d[0]),(xjoints_3d[2],yjoints_3d[2],zjoints_3d[2]),(xjoints_3d[4],yjoints_3d[4],zjoints_3d[4])))
        gt=(54.115166+1100, -1168.320923+27124, 484.712952+1100)
        #ax.scatter(gt[0],gt[1],gt[2], color='y')
        print(xjoints_3d[3], zjoints_3d[3], yjoints_3d[3])
        print(anglesl)
        print(anglesr)
        '''
        # ax show 3d skelecton
        ax.plot([xjoints_3d[k] for k in [10,8,6,5,7,9]], [zjoints_3d[k] for k in [10,8,6,5,7,9]], [yjoints_3d[k] for k in [10,8,6,5,7,9]], 	color='#C71585' )
        ax.plot([xjoints_3d[k] for k in [16,14,12,11,13,15]], [zjoints_3d[k] for k in [16,14,12,11,13,15]], [yjoints_3d[k] for k in [16,14,12,11,13,15]], color='#C71585' )
        ax.plot([xjoints_3d[0] , (xjoints_3d[5]+xjoints_3d[6])/2 ,(xjoints_3d[11]+xjoints_3d[12])/2], [zjoints_3d[0], (zjoints_3d[5]+zjoints_3d[6])/2, (zjoints_3d[11]+zjoints_3d[12])/2], [yjoints_3d[0],  (yjoints_3d[5]+yjoints_3d[6])/2, (yjoints_3d[11]+yjoints_3d[12])/2], color='#C71585' )
        
        # ax4 show 3d skelecton
        #ax4.plot([xjoints_3d[k] for k in [0,2,4,5,3,1]], [zjoints_3d[k] for k in [0,2,4,5,3,1]], [yjoints_3d[k] for k in [0,2,4,5,3,1]], color='orange' )
        #ax4.plot([xjoints_3d[k] for k in [6,8,10,11,9,7]], [zjoints_3d[k] for k in [6,8,10,11,9,7]], [yjoints_3d[k] for k in [6,8,10,11,9,7]], color='orange' )
        #ax4.plot([xjoints_3d[12] , (xjoints_3d[10]+xjoints_3d[11])/2 ,(xjoints_3d[4]+xjoints_3d[5])/2], [zjoints_3d[12], (zjoints_3d[10]+zjoints_3d[11])/2, (zjoints_3d[4]+zjoints_3d[5])/2], [yjoints_3d[12],  (yjoints_3d[10]+yjoints_3d[11])/2, (yjoints_3d[4]+yjoints_3d[5])/2], color='orange' )
        
        # show depth image and the joints
        ax5.imshow(im)
        xjoints_d=[tools.RGBtoD((xjoints[i], yjoints[i]))[0] for i in range(17)]
        yjoints_d=[tools.RGBtoD((xjoints[i], yjoints[i]))[1] for i in range(17)]
        ax5.plot([xjoints_d[k] for k in [10,8,6,5,7,9]], [yjoints_d[k] for k in [10,8,6,5,7,9]],color='#C71585' )
        ax5.plot([xjoints_d[k] for k in [16,14,12,11,13,15]], [yjoints_d[k] for k in [16,14,12,11,13,15]],color='#C71585')
        ax5.plot([xjoints_d[0] , (xjoints_d[5]+xjoints_d[6])/2, (xjoints_d[11]+xjoints_d[12])/2], [yjoints_d[0], (yjoints_d[5]+yjoints_d[6])/2, (yjoints_d[11]+yjoints_d[12])/2],color='#C71585')
        ax5.scatter(xjoints_d, yjoints_d, color='r', s=5)
        
       
        # show color image and the joints with 3d skelecton 
        ax2.imshow(im_c)    
        ax2.plot([xjoints[k] for k in [10,8,6,5,7,9]], [yjoints[k] for k in [10,8,6,5,7,9]],color='#C71585' )
        ax2.plot([xjoints[k] for k in [16,14,12,11,13,15]], [yjoints[k] for k in [16,14,12,11,13,15]],color='#C71585')
        ax2.plot([xjoints[0] , (xjoints[5]+xjoints[6])/2,(xjoints[11]+xjoints[12])/2], [yjoints[0], (yjoints[5]+yjoints[6])/2, (yjoints[11]+yjoints[12])/2],color='#C71585')
        ax2.scatter(xjoints, yjoints, color='r', s=5)
        
        # show the joints' positions
        '''
        for a in [6,12,14,16,8]:
                ax2.text(xjoints[a], yjoints[a], '(%.1f, %.1f, %.1f)'%(xjoints_3d[a],yjoints_3d[a], zjoints_3d[a])+'point'+str(a), color='blue')
        for a in [5,7,11,13,15]:
                ax2.text(xjoints[a], yjoints[a], '(%.1f, %.1f, %.1f)'%(xjoints_3d[a],yjoints_3d[a], zjoints_3d[a])+'point'+str(a), color='orange')
        ax2.text(xjoints[0], yjoints[0], '(%.1f, %.1f, %.1f)'%(xjoints_3d[0],yjoints_3d[0], zjoints_3d[0])+'point'+str(0), color='g')
        ax2.text(xjoints[10], yjoints[10], '(%.1f, %.1f, %.1f)'%(xjoints_3d[10],yjoints_3d[10], zjoints_3d[10])+'point'+str(10), color='g')
        ax2.text(xjoints[9], yjoints[9], '(%.1f, %.1f, %.1f)'%(xjoints_3d[9],yjoints_3d[9], zjoints_3d[9])+'point'+str(9), color='g')
        '''
        for a in [6,12,14,16,8]:
                ax2.text(xjoints[a]-35, yjoints[a], str(a).zfill(2), color='blue')
        for a in [5,7,11,13,15]:
                ax2.text(xjoints[a], yjoints[a], str(a).zfill(2), color='orange')
        ax2.text(xjoints[0]+10, yjoints[0]-10,str(0).zfill(2), color='g')
        ax2.text(xjoints[10]-35, yjoints[10], str(10).zfill(2), color='blue')
        ax2.text(xjoints[9], yjoints[9], str(9).zfill(2), color='orange')
   
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
show_angle3d('2', [frame, frame+1])
sys.exit(1)
