import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import math
import sys
import cv2
from mpl_toolkits.mplot3d import Axes3D
import json
import tools
from tqdm import tqdm
import os
import re
from scipy import signal


def show_result(nb_video, point, frames):
    result=pd.read_csv('testVideos/test'+str(nb_video)+'/test'+str(nb_video)+'_OpenPose_'+point+'.csv')
    # print(pd.DataFrame(result))
    
    fig=plt.figure()

    if(point=='angles'):
    
        ax_left=fig.add_subplot(211)    
        ax_left.set_title('3d OpenPose')

        ax_left.set_xlabel('Frame')
        ax_left.set_ylabel('Angle_left')
        # ax_left.set_xticks([])
        # ax_left.set_yticks([])
        angles=[]
        for i in result['angle_left'][frames[0]:frames[1]]:
            if i == 'NO':
                i=last
            last=i    
            angles.append(180-float(i))   
        ax_left.plot(np.array(result['frame'][frames[0]:frames[1]]),np.array(angles), color='b')#, marker='.')
       
        ax_right=fig.add_subplot(212)
        ax_right.set_xlabel('Frame')
        ax_right.set_ylabel('Angle_right')
        # ax_right.set_xticks([])
        # ax_right.set_yticks([])
        angles=[]
        for i in result['angle_right'][frames[0]:frames[1]]:
            if i == 'NO':
                i=last
            last=i    
            angles.append(180-float(i))   
        
        # ax_left.plot(np.array(result['frame'][frames[0]:frames[1]]),np.array(angles), color='r', marker='.')
        ax_right.plot(np.array(result['frame'][frames[0]:frames[1]]),np.array(angles), color='r')#, marker='.')

        #plt.show()

    else:
    
        ax_position=fig.add_subplot(211)  
        ax_position.set_title('x and y of '+point)
        ax_position.set_xlabel('Frame')
        ax_position.set_ylabel('Position')
        
        x=[]
        y=[]
        for i in result['x2d_'+point[5:]][frames[0]:frames[1]]:
            if i == 'NO':
                i=last
            last=i    
            x.append(float(i))  
        for i in result['y2d_'+point[5:]][frames[0]:frames[1]]:
            if i == 'NO':
                i=last
            last=i    
            y.append(float(i))   
            
        ax_position.plot(np.array(result['frame'][frames[0]:frames[1]]),np.array(x), label="x", color='b')#, marker='.')
        ax_position.plot(np.array(result['frame'][frames[0]:frames[1]]),np.array(y), label="y", color='r')#, marker='.')
       
        ax_precision=fig.add_subplot(212)  
        ax_precision.set_title('Precision of '+point)
        ax_precision.set_xlabel('Frame')
        ax_precision.set_ylabel('Precision')

        pre=[]

        for i in range(frames[0],frames[1]):
            if result['x2d_'+point[5:]][i] == 'NO':
                result['x2d_'+point[5:]][i]=last_x
            last_x=float(result['x2d_'+point[5:]][i])

            if result['y2d_'+point[5:]][i] == 'NO':
                result['y2d_'+point[5:]][i]=last_y
            last_y=float(result['y2d_'+point[5:]][i])

            # precision=get_distance((last_x, last_y),(gt_x, gt_y))
            # pre.append(precision)
            # pre=normal(pre)

        # ax_precision.plot(np.array(result['frame'][frames[0]:frames[1]]),np.array(pre), label="precision", color='b', marker='.')
        plt.title('Precision of '+point)

def get_distance(p1,p2):   
    return math.sqrt(sum([(p1[i]-p2[i])**2 for i in range(len(p1))]))

def normal(l):
    return [(i-min(l))/(max(l)-min(l)) for i in l]

def show_angle3d(nb_vedio, frames): 

    files=os.listdir('testVideos/test'+nb_vedio+'/') 
    for i in files:
        if (len(re.findall('.*C\.json', i))!=0):
            filejson=i
        if (len(re.findall('.*D.mp4', i))!=0):
            filedepth=i

    print(filejson)
    fig=plt.figure()
    ax=fig.add_subplot(211)
    ax2=fig.add_subplot(212)
    ax.set_title('3d kinect OpenPose')
    ax.set_xlabel('Frame')
    ax.set_ylabel('Angle_left')
    ax2.set_xlabel('Frame')
    ax2.set_ylabel('Angle_right')

    with open('testVideos/test'+nb_vedio+'/'+filejson) as json_data:
        d = json.load(json_data)
    v=cv2.VideoCapture('testVideos/test'+nb_vedio+'/'+filedepth)

    anglesl=[]
    anglesr=[]

    for t in tqdm(range(frames[0],frames[1])):
        #print(t)
        v.set(cv2.CAP_PROP_POS_FRAMES, t)
        ret, im=v.read()
    

        #中值滤波
        if t>100:
            img_m=cv2.medianBlur(im,7)
            font=cv2.FONT_HERSHEY_SIMPLEX
        else:
            img_m=cv2.medianBlur(im,5)
            font=cv2.FONT_HERSHEY_SIMPLEX
       
        '''
        for i in range(800,980,2):
            for j in range(300,860,5):
                a=RGBto3D((i,j),im)
                x.append(a[0])
                y.append(a[1])
                z.append(a[2])
            print(i)
        #ax.scatter(x,z,y)
        '''
        if len(d['frames'][t])!=0:
            xjoints=d['frames'][t][0]['pose2d'][:18]
            yjoints=d['frames'][t][0]['pose2d'][18:]
            zjoints=[]
    
            for i in range(18):
                joints=tools.RGBto3D((xjoints[i], yjoints[i]), img_m)
                #joints=tools.RGBto3D((xjoints[i], yjoints[i]), im)
                #joints=tools.RGBto3D((xjoints[i], yjoints[i]), im, True,5)
                #joints=tools.RGBto3D((xjoints[i], yjoints[i]), img_m)
                xjoints[i]=joints[0]
                yjoints[i]=joints[1]
                zjoints.append(joints[2])

        anglesl.append(180-tools.angle((xjoints[11], yjoints[11],zjoints[11]),(xjoints[12], yjoints[12],zjoints[12]),(xjoints[13], yjoints[13],zjoints[13])))
        anglesr.append(180-tools.angle((xjoints[8], yjoints[8],zjoints[8]),(xjoints[9], yjoints[9],zjoints[9]),(xjoints[10], yjoints[10],zjoints[10])))
        
        
        # angle 2d
        # anglesl.append(180-tools.angle((yjoints[1],zjoints[1]),(yjoints[3],zjoints[3]),(yjoints[5],zjoints[5])))
        # anglesr.append(180-tools.angle((yjoints[0],zjoints[0]),(yjoints[2],zjoints[2]),(yjoints[4],zjoints[4])))
        
        '''
        print(xjoints)
        print(yjoints)
        print(zjoints)
    ax2.scatter(xjoints, zjoints, yjoints, color='r')
    '''    
    v.release()
    
    #b, a = signal.butter(8, 0.3, 'lowpass') 
    #anglesl = signal.filtfilt(b, a, anglesl) 
    #anglesr = signal.filtfilt(b, a, anglesr)   
    frames=range(frames[0],frames[1])
    ax.plot(frames, anglesl)
    print(anglesl)
    print(anglesr)
    ax2.plot(frames, anglesr, color='r')

def show_gt(nb_video, frames):
    
    files=os.listdir('testVedios/test'+nb_video+'/') 
    for i in files:
        if (len(re.findall('julia104.*'+'left', i))!=0):
            filename1=i
        if (len(re.findall('julia104.*'+'right', i))!=0):
            filename2=i

    print(filename1)
    print(filename2)
    data1=pd.read_csv('testVedios/test'+nb_video+'/'+filename1)
    data2=pd.read_csv('testVedios/test'+nb_video+'/'+filename2)
    data3= pd.read_csv('testVedios/test'+nb_video+'/tempstams.csv')

    data1=(pd.DataFrame(data1))
    data2=(pd.DataFrame(data2))
    data3=(pd.DataFrame(data3))
    frame=data3['frame']
    time=data3['time']
    times=[]

    for i in time:
        i=round((i-44471900000)/10)
        times.append(i)
    '''
    print(frames[0])
    fields=range(times[frames[0]]-350, times[frames[1]]-350)
    print(fields)
    '''

    angleX_l=data1['X']
    
    angleY=data1['Y']
    angleZ=data1['Z']
    field=data1['field']
    angleX_r=data2['X']

    fig=plt.figure()
    ax=fig.add_subplot(211)   
    ax2=fig.add_subplot(212) 

    ax.set_title('GT : Lfet Knee Angles ')
    ax.set_xlabel('Field')
    ax.set_ylabel('Angle')

    ax2.set_title('GT : Right Knee Angles ')
    ax2.set_xlabel('Field')
    ax2.set_ylabel('Angle')
    # ax.set_xticks([])
    # axleft.set_yticks([])
    ax.plot(field, angleX_l, color='b', marker='.', label='Angle_X')
    ax2.plot(field, angleX_r, color='r', marker='.', label='Angle_X')
    #ax.plot(field, angleY, color='g', marker='.', label='Angle_Y')
    #ax.plot(field, angleZ, color='b', marker='.', label='Angle_Z')
    

if __name__=="__main__":
    if len(sys.argv)!=5:
        print("Usage: python3 show_result.py nb_video point frame_start frame_end. ex : 1 point12 50 150")
        sys.exit(1)

    nb_video = int(sys.argv[1])
    point=sys.argv[2]
    frames=[]
    frames.append(int(sys.argv[3]))
    frames.append(int(sys.argv[4]))
    #show_gt(str(nb_video), frames)
    #show_result(nb_video, point, frames)
    show_angle3d(str(nb_video),frames)
    plt.show()
    sys.exit(1)
    