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

def get_distance(p1,p2):   
    return math.sqrt(sum([(p1[i]-p2[i])**2 for i in range(len(p1))]))

def normal(l):
    return [(i-min(l))/(max(l)-min(l)) for i in l]

def show_angle3d(nb_video, frames): 

    files=os.listdir('testVideos/test'+nb_video+'/') 
    for i in files:
        if (len(re.findall('.*C\.json', i))!=0):
            filejson=i
        if (len(re.findall('.*D.mp4', i))!=0):
            filedepth=i
            number=filedepth[:-5]
        if (len(re.findall('_PifPaf_joints_3DKinect_front.csv', i))!=0):
            filedis=i
    print(number)
    print(filejson)
    print(filedis)
    print('testVideos'+'/test'+nb_video+'/'+number+'_PifPaf_joints_3DKinect_back.csv')
    disdata=pd.DataFrame(pd.read_csv('testVideos/test'+nb_video+'/'+filedis))
    fig=plt.figure()
    ax=fig.add_subplot(211)
    ax2=fig.add_subplot(212)
    ax.set_title('3d kinect PifPaf_Original')
    ax.set_xlabel('Frame')
    ax.set_ylabel('Angle_left')
    ax2.set_xlabel('Frame')
    ax2.set_ylabel('Angle_right')

    with open('testVideos/test'+nb_video+'/'+filejson) as json_data:
        d = json.load(json_data)
    v=cv2.VideoCapture('testVideos/test'+nb_video+'/'+filedepth)

    anglesl=[]
    anglesr=[]
    points3dx=[[] for p in range(17)]
    points3dy=[[] for p in range(17)]
    points3dz=[[] for p in range(17)]
    points2dx=[[] for p in range(17)]
    points2dy=[[] for p in range(17)]
    points2ddx=[[] for p in range(17)]
    points2ddy=[[] for p in range(17)]
    akdis=[]
    kndis=[]
    step=[]

    bad_frame=[0]*(frames[1]-frames[0])
    l_kn_ak=[]
    r_kn_ak=[]   

    for t in tqdm(range(frames[0],frames[1])):
        #print(t)
        v.set(cv2.CAP_PROP_POS_FRAMES, t)
        ret, im=v.read()
    
      
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
            xjoints2d=d['frames'][t][0]['pose2d'][:17]
            yjoints2d=d['frames'][t][0]['pose2d'][17:]
            
            zjoints3d=[]
            xjoints3d=[]
            yjoints3d=[]

            xjoints2dd=[]
            yjoints2dd=[]
            leg=['z_las','z_ras','z_lkn','z_rkn','z_lak','z_rak']
            for i in range(17):
                if i in [11,13,15,12,14,16]:
                    z3d=float(disdata[leg[i-11]][disdata['frames']==t])
                    print(z3d)
                    joints=tools.RGBto3D((xjoints2d[i], yjoints2d[i], z3d), im, t)
                    xjoints3d.append(joints[0])
                    yjoints3d.append(joints[1])
                    zjoints3d.append(joints[2])

                else:
                    joints=tools.RGBto3D((xjoints2d[i], yjoints2d[i]), im, t, True, 7)
                    xjoints3d.append(joints[0])
                    yjoints3d.append(joints[1])
                    zjoints3d.append(joints[2])
                
                joints2dd=tools.RGBtoD((xjoints2d[i], yjoints2d[i]), t)    
                xjoints2dd.append(joints2dd[0])
                yjoints2dd.append(joints2dd[1])

       
        anglesl.append(180-tools.angle((xjoints3d[11],yjoints3d[11],zjoints3d[11]),(xjoints3d[13],yjoints3d[13],zjoints3d[13]),(xjoints3d[15],yjoints3d[15],zjoints3d[15]),False))
        anglesr.append(180-tools.angle((xjoints3d[12],yjoints3d[12],zjoints3d[12]),(xjoints3d[14],yjoints3d[14],zjoints3d[14]),(xjoints3d[16],yjoints3d[16],zjoints3d[16]),False)) 
        # static analysis
        # save the important information:dis between ankles, as height, leg length
        l_kn_ak.append(tools.get_distance((xjoints3d[12],yjoints3d[12],zjoints3d[12]),(xjoints3d[13],yjoints3d[13],zjoints3d[13])))
        r_kn_ak.append(tools.get_distance((xjoints3d[9],yjoints3d[9],zjoints3d[9]),(xjoints3d[10],yjoints3d[10],zjoints3d[10])))
        dak=(zjoints3d[10]-zjoints3d[13])
        dkn=(zjoints3d[9]-zjoints3d[12])
        akdis.append(dak)
        kndis.append(dkn)
        for p in range(17):  
            points3dx[p].append(xjoints3d[p])
            points3dy[p].append(yjoints3d[p])
            points3dz[p].append(zjoints3d[p])
            points2dx[p].append(xjoints2d[p])
            points2dy[p].append(yjoints2d[p])
            points2ddx[p].append(xjoints2dd[p])
            points2ddy[p].append(yjoints2dd[p])
    v.release()
    
    #b, a = signal.butter(8, 0.3, 'lowpass') 
    #anglesl = signal.filtfilt(b, a, anglesl) 
    #anglesr = signal.filtfilt(b, a, anglesr)   
    frames=range(frames[0],frames[1])
    ax.plot(frames, anglesl)
    
    ax2.plot(frames, anglesr, color='r')
   
    data2d={}
    data={}
    data2dd={}
    data2dd['frames']=frames
    data2d['frames']=frames
    data['frames']=frames
    data['kangle_l']=anglesl
    data['kangle_r']=anglesr
    data['akdis']=akdis
    data['kndis']=kndis
    data['l_kn_ak']=l_kn_ak
    data['r_kn_ak']=r_kn_ak
    data['bad_frame']=bad_frame

    j=['head','leye','reye','lear','rear','lsh','rsh','lel','rel','lwr','rwr','las','ras','lkn','rkn','lak','rak']   
    
    for p in range(17):
        data['x_'+j[p]]=points3dx[p]
        data['y_'+j[p]]=points3dy[p]
        data['z_'+j[p]]=points3dz[p]
        data2d['x_'+j[p]]=points2dx[p]
        data2d['y_'+j[p]]=points2dy[p]
        data2dd['x_'+j[p]]=points2ddx[p]
        data2dd['y_'+j[p]]=points2ddy[p]
        data=pd.DataFrame(data)
        data2d=pd.DataFrame(data2d)
        data2dd=pd.DataFrame(data2dd)
    if frames[0]>250:
        data.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_PifPaf_joints_3DKinect_back.csv',encoding='gbk')
        data2d.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_PifPaf_joints_2DColor_back.csv',encoding='gbk')        
        data2dd.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_PifPaf_joints_2DDepth_back.csv',encoding='gbk')
        #data1=pd.DataFrame({'frame':frames, 'angle_left':anglesl, 'angle_right':anglesr})
        #data1.to_csv('testVedios'+'/test'+nb_vedio+'/'+number+'_LCR-NET_angles_3DKinect_back.csv',encoding='gbk')
    
    else:
        data2dd.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_PifPaf_joints_2DDepth_front.csv',encoding='gbk')
        data2d.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_PifPaf_joints_2DColor_front.csv',encoding='gbk')
        data.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_PifPaf_joints_3DKinect_front.csv',encoding='gbk')
        #data1=pd.DataFrame({'frame':frames, 'angle_left':anglesl, 'angle_right':anglesr})
       
def show_gt(nb_video, frames):
    
    files=os.listdir('testVideos/test'+nb_video+'/') 
    for i in files:
        if (len(re.findall('julia104.*'+'left', i))!=0):
            filename1=i
        if (len(re.findall('julia104.*'+'right', i))!=0):
            filename2=i

    print(filename1)
    print(filename2)
    data1=pd.read_csv('testVideos/test'+nb_video+'/'+filename1)
    data2=pd.read_csv('testVideos/test'+nb_video+'/'+filename2)
  
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
    show_angle3d(str(nb_video),frames)
    plt.show()
    sys.exit(1)
    