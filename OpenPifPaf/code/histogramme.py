import cv2
import numpy as np
import matplotlib.pyplot as plt
import tools
import json
import pylab as pl
import scipy.signal as signal
import os
import re

def his_image(im, size, joint, data):


    joints={'lankle': 15, 'rankle': 16, 'lknee': 13, 'rknee': 14, 'lthi': 11, 'rthi': 12}
    # médian
    img_m=cv2.medianBlur(im,5)
    font=cv2.FONT_HERSHEY_SIMPLEX
    img_m=img_m[0:828, 0:512]
    '''
    img_m_h=img_m[0:424, 0:512]
    img_m_b=img_m[424:828, 0:512]
    for i in range(424):
        for j in range(512):
            img_m[i,j]=img_m_h[i,j]*256/6+img_m_b[i,j]
    '''
    xjoints=data[0:17]
    yjoints=data[17:]
    x=xjoints[joints[joint]]
    y=yjoints[joints[joint]] 
    (x_d, y_d)=tools.RGBtoD((x, y))
    ndg_h1=img_m[y_d, x_d][0]# Original Depth_high
    ndg_b1=img_m[y_d+424, x_d][0]# Depth Original_low
    ng=[]
    #print(img_m[(y_d-int((size-1)/2)):(y_d+int((size-1)/2)),(x_d-int((size-1)/2)):(x_d+int((size-1)/2))] )
    for i in range(y_d-int((size-1)/2), y_d+int((size-1)/2)+1):
        for j in range(x_d-int((size-1)/2), x_d+int((size-1)/2)+1):
            z0=(img_m[i,j]*256/6+img_m[i+424,j])[0]/10
            if z0>200 and z0<700:
                ng.append(int(round(z0)))
    
    print(len(ng))
  

    ngh=[0]*700
    for h in set(ng):
        ngh[h]=ng.count(h)

    zm=ngh.index(max(ngh))*10
    print(zm)

    return (zm, ndg_h1*256/6+ndg_b1)

def his_video(nb_video, frames):
    files=os.listdir('testVideos/test'+nb_video+'/') 
    for i in files:
        if (len(re.findall('.*C\.json', i))!=0):
            filejson=i
        if (len(re.findall('.*D.mp4', i))!=0):
            filedepth=i
    v=cv2.VideoCapture('testVideos/test'+nb_video+'/'+filedepth)
    with open('testVideos/test'+nb_video+'/'+filejson) as json_data:
        d = json.load(json_data)

    v.set(cv2.CAP_PROP_POS_FRAMES, frames[0])
    dis_lankle=[]
    dis_lankle0=[]
    dis_lknee=[]
    dis_lknee0=[]
    dis_lthi=[]
    dis_lthi0=[]

    dis_lankle_m=[]
    dis_lankle_mm=[]
    dis_lknee_m=[]
    dis_lknee_mm=[]
    dis_lthi_m=[]
    dis_lthi_mm=[]

    for frame in range(frames[0], frames[1]):
        ret, im=v.read()          
        data=d['frames'][frame][0]['pose2d']

        hist=his_image(im, 7, 'lankle', data)
        dis_lankle.append(hist[0])
        dis_lankle0.append(hist[1])

        hist=his_image(im,7, 'lknee', data)
        dis_lknee.append(hist[0])
        dis_lknee0.append(hist[1])

        hist=his_image(im, 7, 'lthi', data)
        dis_lthi.append(hist[0])
        dis_lthi0.append(hist[1])
        # médian
        img_m=cv2.medianBlur(im,5)
        font=cv2.FONT_HERSHEY_SIMPLEX
        hist=his_image(img_m, 7, 'lankle', data)
        dis_lankle_mm.append(hist[0])
        dis_lankle_m.append(hist[1])

        hist=his_image(img_m,7, 'lknee', data)
        dis_lknee_mm.append(hist[0])
        dis_lknee_m.append(hist[1])

        hist=his_image(img_m, 7, 'lthi', data)
        dis_lthi_mm.append(hist[0])
        dis_lthi_m.append(hist[1])
    fig=plt.figure()

    ax=fig.add_subplot(221)
    ax.set_title('7*7 Hist_MAX_Left Ankle(blue), Knee(orange), Thigh(green)')
    ax.plot(range(frames[0], frames[1]), dis_lankle)
    ax.plot(range(frames[0], frames[1]), dis_lknee)
    ax.plot(range(frames[0], frames[1]), dis_lthi)
    
    ax2=fig.add_subplot(222)
    ax2.set_title('7*7 Original_Left Ankle(blue), Knee(orange), Thigh(green) ')
    ax2.plot(range(frames[0], frames[1]), dis_lankle0)
    ax2.plot(range(frames[0], frames[1]), dis_lknee0)
    ax2.plot(range(frames[0], frames[1]), dis_lthi0)

    ax3=fig.add_subplot(223)
    ax3.set_title('7*7 Median_Left Ankle(blue), Knee(orange), Thigh(green) ')
    ax3.plot(range(frames[0], frames[1]), dis_lankle_m)
    ax3.plot(range(frames[0], frames[1]), dis_lknee_m)
    ax3.plot(range(frames[0], frames[1]), dis_lthi_m)
    

    ax4=fig.add_subplot(224)
    ax4.set_title('7*7 Median+Max_Left Ankle(blue), Knee(orange), Thigh(green)')
    ax4.plot(range(frames[0], frames[1]), dis_lankle_mm)
    ax4.plot(range(frames[0], frames[1]), dis_lknee_mm)
    ax4.plot(range(frames[0], frames[1]), dis_lthi_mm)
    plt.show()
    plt.show()


his_video('2', [70, 135])