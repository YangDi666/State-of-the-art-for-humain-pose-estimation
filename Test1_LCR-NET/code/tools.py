import cv2
import matplotlib.pylab as plt
import numpy as np
import math
import pylab as pl
import scipy.signal as signal

def RGBtoD(p):
    CAMERA={
    'FX_C':1081.3720703125,
    'FY_C':-1081.3720703125,
    'CX_C':960.5,
    'CY_C':539.5,
    'FX_D':366.864685058594,
    'FY_D':-366.864685058594,
    'CX_D':263.148010253906, 
    'CY_D':200.292007446289}

    x_c=p[0]
    y_c=p[1]
    x_d=round((x_c-CAMERA['CX_C'])/CAMERA['FX_C']*CAMERA['FX_D']+CAMERA['CX_D']+4)
    y_d=round((y_c-CAMERA['CY_C'])/CAMERA['FY_C']*CAMERA['FY_D']+CAMERA['CY_D'])
    #print(x_d)
    #print(y_d)
    #print(type(im[y_d][x_d][0]))
    #print(im[y_d+424][x_d][0])
   
    return (x_d, y_d)

def filter(p, im, size):
    s=(size-1)/2
    (x_d, y_d)=RGBtoD(p)
    win=[im[i,j] for i in range(y_d-s, y_d+s+1) for j in range(x_d-s, x_d+s+1)]
    for k in win:
        if (k>=0 and k<=23) or k>175:
            win.remove(k)
    win=np.array(win)
    return np.median(win)

def RGBto3D(p, im, filter=False, size=0):
    CAMERA={
    'FX_C':1081.3720703125,
    'FY_C':-1081.3720703125,
    'CX_C':960.5,
    'CY_C':539.5,
    'FX_D':366.864685058594,
    'FY_D':-366.864685058594,
    'CX_D':263.148010253906, 
    'CY_D':200.292007446289}

    x_c=p[0]
    y_c=p[1]
    x_d=(x_c-CAMERA['CX_C'])/CAMERA['FX_C']*CAMERA['FX_D']+CAMERA['CX_D']+4
    y_d=(y_c-CAMERA['CY_C'])/CAMERA['FY_C']*CAMERA['FY_D']+CAMERA['CY_D']
    #print(x_d)
    #print(y_d)
    #print(type(im[y_d][x_d][0]))
    #print(im[y_d+424][x_d][0])
    if filter:
        z=his_image(im, size, p)[0]
    else:
        #print(im[round(y_d)][round(x_d)][0])
        z=im[round(y_d)][round(x_d)][0]*256/6+im[round(y_d+424)][round(x_d)][0]
    '''
    if(z==0):
        z1=max([im[y_d+i][x_d+j][0] for i in range(-2,3) for j in range(-2,3)])
        z0=min([im[y_d+i][x_d+j][0] for i in range(-2,3) for j in range(-2,3)])
    
        z=z1*256+z0    
    '''
    x=(x_d-CAMERA['CX_D'])*z/CAMERA['FX_D']
    y=(y_d-CAMERA['CY_D'])*(z)/CAMERA['FY_D']
    
    return (x, y, z)

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

def v2i(cap, frame, save=False): 
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame)  # 设置帧数标记
    ret, im = cap.read()  # read方法返回一个布尔值和一个视频帧
    if ret: 
        if save:
            cv2.imwrite("test1/img/" + str(frame) + "C.jpg", im)
        return im
    else:
        return 'No image!!'
    
def his_image(im, size, p):

    # médian
    #img_m=cv2.medianBlur(im,5)
    #font=cv2.FONT_HERSHEY_SIMPLEX
    img_m=im[0:828, 0:512]
    '''
    img_m_h=img_m[0:424, 0:512]
    img_m_b=img_m[424:828, 0:512]
    for i in range(424):
        for j in range(512):
            img_m[i,j]=img_m_h[i,j]*256/6+img_m_b[i,j]
    '''
   
    x=p[0]
    y=p[1]
    (x_d, y_d)=RGBtoD((x, y))
    ndg_h1=img_m[y_d, x_d][0]# Original Depth_high
    ndg_b1=img_m[y_d+424, x_d][0]# Depth Original_low
    print(ndg_h1, ndg_b1)
    #print(img_m[(y_d-int((size-1)/2)):(y_d+int((size-1)/2)),(x_d-int((size-1)/2)):(x_d+int((size-1)/2))] )
    ng=[]
    #print(img_m[(y_d-int((size-1)/2)):(y_d+int((size-1)/2)),(x_d-int((size-1)/2)):(x_d+int((size-1)/2))] )
    for i in range(y_d-int((size-1)/2), y_d+int((size-1)/2)+1):
        for j in range(x_d-int((size-1)/2), x_d+int((size-1)/2)+1):
            z0=(img_m[i,j]*256/6+img_m[i+424,j])[0]/10
            if z0>120 and z0<750:
                ng.append(int(round(z0)))
    
    print(len(ng))
  

    ngh=[0]*750
    for h in set(ng):
        ngh[h]=ng.count(h)

    zm=ngh.index(max(ngh))*10
    print(zm)
   

    return (zm, ndg_h1*256/6+ndg_b1)
