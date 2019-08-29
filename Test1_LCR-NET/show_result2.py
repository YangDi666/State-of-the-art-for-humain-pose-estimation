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
    result=pd.read_csv('testVedios/test'+str(nb_video)+'/test'+str(nb_video)+'_LCR-NET_'+point+'.csv')
    # print(pd.DataFrame(result))
    
    fig=plt.figure()

    if(point=='angles'):
    
        ax_left=fig.add_subplot(211)    
        ax_left.set_title('3d LCR-NET')

        ax_left.set_xlabel('Frame')
        ax_left.set_ylabel('Angle_left')
        # ax_left.set_xticks([])
        # ax_left.set_yticks([])
        angles=[]
        for i in result['angle_left'][frames[0]:frames[1]]:
            if i == 'No':
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
            if i == 'No':
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
            if i == 'No':
                i=last
            last=i    
            x.append(float(i))  
        for i in result['y2d_'+point[5:]][frames[0]:frames[1]]:
            if i == 'No':
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
            if result['x2d_'+point[5:]][i] == 'No':
                result['x2d_'+point[5:]][i]=last_x
            last_x=float(result['x2d_'+point[5:]][i])

            if result['y2d_'+point[5:]][i] == 'No':
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

    files=os.listdir('testVedios/test'+nb_vedio+'/') 
    for i in files:
        if (len(re.findall('.*C\.json', i))!=0):
            filejson=i
        if (len(re.findall('.*D.mp4', i))!=0):
            filedepth=i
            number=filedepth[:-5]
        if (len(re.findall('_LCR-NET_joints_3DKinect_front.csv', i))!=0):
            filedis=i
    print(number)
    print(filedis)
    print(filejson)
    disdata=pd.DataFrame(pd.read_csv('testVedios/test'+nb_vedio+'/'+filedis))
    fig=plt.figure()
    ax=fig.add_subplot(211)
    ax2=fig.add_subplot(212)
    ax.set_title('3d kinect LCR-NET_Original')
    ax.set_xlabel('Frame')
    ax.set_ylabel('Angle_left')
    ax2.set_xlabel('Frame')
    ax2.set_ylabel('Angle_right')

    with open('testVedios/test'+nb_vedio+'/'+filejson) as json_data:
        d = json.load(json_data)
    v=cv2.VideoCapture('testVedios/test'+nb_vedio+'/'+filedepth)

    anglesl=[]
    anglesr=[]
    points3dx=[[] for p in range(13)]
    points3dy=[[] for p in range(13)]
    points3dz=[[] for p in range(13)]
    points2dx=[[] for p in range(13)]
    points2dy=[[] for p in range(13)]
    points2ddx=[[] for p in range(13)]
    points2ddy=[[] for p in range(13)]

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
    
      
        img_m=cv2.medianBlur(im,7)
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
            xjoints2d=d['frames'][t][0]['pose2d'][:13]
            yjoints2d=d['frames'][t][0]['pose2d'][13:]
            xjoints3d=[]
            yjoints3d=[]
            zjoints3d=[]
            xjoints2dd=[]
            yjoints2dd=[]
    ###!!!!!!!!!11111!!!!
            leg=['z_rak','z_lak','z_rkn','z_lkn','z_ras','z_las']
            for i in range(13):
                if i<=5:
                    z3d=float(disdata[leg[i]][disdata['frames']==t])
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
        for p in range(13):  
            points3dx[p].append(xjoints3d[p])
            points3dy[p].append(yjoints3d[p])
            points3dz[p].append(zjoints3d[p])
            points2dx[p].append(xjoints2d[p])
            points2dy[p].append(yjoints2d[p])
            points2ddx[p].append(xjoints2dd[p])
            points2ddy[p].append(yjoints2dd[p])
    
        anglesl.append(180-tools.angle((xjoints3d[1],yjoints3d[1],zjoints3d[1]),(xjoints3d[3],yjoints3d[3],zjoints3d[3]),(xjoints3d[5],yjoints3d[5],zjoints3d[5]), False)) 
        anglesr.append(180-tools.angle((xjoints3d[0],yjoints3d[0],zjoints3d[0]),(xjoints3d[2],yjoints3d[2],zjoints3d[2]),(xjoints3d[4],yjoints3d[4],zjoints3d[4]), False))
       
        # static analysis
        # save the important information:dis between ankles, as height, leg length
        l_kn_ak.append(tools.get_distance((xjoints3d[1],yjoints3d[1],zjoints3d[1]),(xjoints3d[3],yjoints3d[3],zjoints3d[3])))
        r_kn_ak.append(tools.get_distance((xjoints3d[0],yjoints3d[0],zjoints3d[0]),(xjoints3d[2],yjoints3d[2],zjoints3d[2])))
        dak=(zjoints3d[0]-zjoints3d[1])
        dkn=(zjoints3d[2]-zjoints3d[3])
        akdis.append(dak)
        kndis.append(dkn)
           
        # dynamic analysis
        # gen qian mian de zhen xiang bi jiao
        # Model : step automatic by Vicon !!!!front back!!!!! condition 1 2 3
        # dis>0 : left joint is in front, dis<0 : right joint is in front
        
        if dkn<=0 and dak>-100:
            step.append(0)
        elif dak<=-100 and dkn<0:
            step.append(1)
        elif dkn>=0 and dak<100:
            step.append(2)
        elif dak>=100 and dkn>0:
            step.append(3)
        else:
            step.append(-1)
        
        # find the wrong frame
        # +++++++++++
        # correct the wrong ponts
        # +++++++++++

        
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
    ax.plot(frames, anglesl, marker='.')
    
    ax2.plot(frames, anglesr, color='r',  marker='.')#, marker='.')
    #for i in range(50): y1.append(i) # 每迭代一次，将i放入y1中画出来 ax.cla() # 清除键 ax.bar(y1, label='test', height=y1, width=0.3) ax.legend() plt.pause(0.1)
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
    print(len(step))
    data['step']=step

    j=['rak','lak','rkn','lkn','ras','las','rwr','lwr','rel','lel','rsh','lsh','head']   
    
    for p in range(13):
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
        data.to_csv('testVedios'+'/test'+nb_vedio+'/'+number+'_LCR-NET_joints_3DKinect_back.csv',encoding='gbk')
        data2d.to_csv('testVedios'+'/test'+nb_vedio+'/'+number+'_LCR-NET_joints_2DColor_back.csv',encoding='gbk')        
        data2dd.to_csv('testVedios'+'/test'+nb_vedio+'/'+number+'_LCR-NET_joints_2DDepth_back.csv',encoding='gbk')
        #data1=pd.DataFrame({'frame':frames, 'angle_left':anglesl, 'angle_right':anglesr})
        #data1.to_csv('testVedios'+'/test'+nb_vedio+'/'+number+'_LCR-NET_angles_3DKinect_back.csv',encoding='gbk')
    
    else:
        data2dd.to_csv('testVedios'+'/test'+nb_vedio+'/'+number+'_LCR-NET_joints_2DDepth_front.csv',encoding='gbk')
        data2d.to_csv('testVedios'+'/test'+nb_vedio+'/'+number+'_LCR-NET_joints_2DColor_front.csv',encoding='gbk')
        data.to_csv('testVedios'+'/test'+nb_vedio+'/'+number+'_LCR-NET_joints_3DKinect_front.csv',encoding='gbk')
        #data1=pd.DataFrame({'frame':frames, 'angle_left':anglesl, 'angle_right':anglesr})
        #data1.to_csv('testVedios'+'/test'+nb_vedio+'/'+number+'_LCR-NET_angles_3DKinect_front.csv',encoding='gbk')
    

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
    #data3= pd.read_csv('testVedios/test'+nb_video+'/tempstams.csv')

    data1=(pd.DataFrame(data1))
    data2=(pd.DataFrame(data2))
    #data3=(pd.DataFrame(data3))
    #frame=data3['frame']
    #time=data3['time']
    times=[]
    '''
    for i in time:
        i=round((i-44471900000)/10)
        times.append(i)
    
    print(frames[0])
    fields=range(times[frames[0]]-350, times[frames[1]]-350)
    print(fields)
    '''

    angleX_l=data1['X_ag']
    
    angleY=data1['Y']
    angleZ=data1['Z']
    field=data1['field']
    angleX_r=data2['X_ag']

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
    ax.plot(field, angleX_l, color='b', label='Angle_X')
    ax2.plot(field, angleX_r, color='r', label='Angle_X')
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
    
    #show_result(nb_video, point, frames)
    show_angle3d(str(nb_video),frames)
    #show_gt(str(nb_video), frames)
    plt.show()
    sys.exit(1)
    