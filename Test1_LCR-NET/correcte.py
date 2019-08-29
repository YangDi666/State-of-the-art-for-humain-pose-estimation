import pandas as pd 
import os
import sys
import re
import matplotlib.pyplot as plt 
import tools
import numpy as np
import statistics
import scipy.signal
import math

def linear_insert(a, b, n, k):
    return (a*(n-k)+k*b)/n
def maxv(a, b):
    if(a>b):
        return a
    else:
        return b

def minv(a, b):
    if(a>b):
        return b
    else:
        return a

# first correction for the points increasing
def correct1(z, badframe, joint, size):
    begin=0
    end=len(z)-1
    
    if joint!='ak':
        for i in range(begin+size, end-size+1):
             if (z[i]-z[i-1])*(z[i+1]-z[i])<0:
                 b=list(range(-size,size+1))
                 b.remove(0)
                 print(i)
                 z[i]=sum([z[i+j]*abs(1/j) for j in b])/sum([abs(1/j) for j in b])
        return
    while badframe[begin]!=0:
        begin+=1
    while badframe[end]!=0:
        end-=1
    i=begin+2
    j=i+1
    while(j<end-1  and badframe[j]!=0):    
        j+=1
    window=[0, z[i-2], z[i-1], z[i], z[j]]
    dis=[2,1,0,1,j-i+1]
    k=j+1
    while(i<end-3):
        if j<k: 

            while (k<end-3  and badframe[k]!=0):
                k+=1
       
            window.pop(0)
            window.append(z[k])
            dis[0]=dis[1]+dis[3]
            dis[1]=dis[3]
            dis[2]=0
            dis[3]=dis[4]-dis[3]
            dis[4]=k-i
            
            if window[2]-window[1]>0:     
                #z[i]=window[1]    
                z[i]=sum([window[a]*(1/dis[a]) for a in range(len(dis)) if dis[a]!=0])/sum([1/b for b in dis if b!=0])     
                window[2]=z[i]
                print('w1',i, window, z[i])
                if window[2]-window[1]>0:                    
                    z[i]=window[1]
                    window[2]=z[i]
                    print('w2', i, window)
            i=j
            j=k+1
        if j>k: 

            while (j<end-3  and badframe[j]!=0):
                j+=1
       
            window.pop(0)
            window.append(z[j])
            dis[0]=dis[1]+dis[3]
            dis[1]=dis[3]
            dis[2]=0
            dis[3]=dis[4]-dis[3]
            dis[4]=j-i
            
            if window[2]-window[1]>0:
                #z[i]=window[1]
                z[i]=sum([window[a]*(1/dis[a]) for a in range(len(dis)) if dis[a]!=0])/sum([1/b for b in dis if b!=0])
                window[2]=z[i]
                print('w1',i, window)
                if window[2]-window[1]>0:
                    z[i]=window[1]
                    window[2]=z[i]
                    print('w2', i, window)             
            i=k
            k=j+1

# second crrection: linear insertion for the badframe
def correct2(z, badframe, err_type):
    begin=0
    end=len(z)-1
    while badframe[begin]!=0:
        begin+=1
    while badframe[end]!=0:
        end-=1
    print(begin,end)
    
    if err_type==10:             
        for i in range(begin,end):

            if badframe[i]==10 or badframe[i]==30:
                j=1
                while(badframe[i+j]==10 or badframe[i+j]==30):
                    j+=1 
                for k in range(1, j+1):
                    z[i+k-1]=linear_insert(z[i-1], z[i+j], j+1, k)
    if err_type==11:             
        for i in range(begin,end):

            if badframe[i]==11 or badframe[i]==31:
                j=1
                while(badframe[i+j]==11 or badframe[i+j]==31):
                    j+=1 
                for k in range(1, j+1):
                    z[i+k-1]=linear_insert(z[i-1], z[i+j], j+1, k)

    if err_type==20:
        for i in range(begin,end):

            if badframe[i]==20:
                j=1
                while(badframe[i+j]==20):
                    j+=1 
                for k in range(1, j+1):
                    z[i+k-1]=linear_insert(z[i-1], z[i+j], j+1, k)
    if err_type==21:
        for i in range(begin,end):

            if badframe[i]==21:
                j=1
                while(badframe[i+j]==21):
                    j+=1 
                for k in range(1, j+1):
                    z[i+k-1]=linear_insert(z[i-1], z[i+j], j+1, k)

# third correction: filter low-pass
def filter(a, size, flt_type='mean', sigma=1):
    if flt_type not in ['mean','median', 'gaussian']:
        print('No filter!')
        return a
    elif flt_type!='gaussian':
        b=a[:size]
        window=a[:2*size+1]
        if flt_type=='median':
            b.append(statistics.median(window))
            for i in a[2*size+1:]:   
                window.append(i)
                window.pop(0)
                #b.append(sum(window)/len(window))
                b.append(statistics.median(window))
        else:
            b.append(sum(window)/len(window))
            for i in a[2*size+1:]:
                window.append(i)
                window.pop(0)
                b.append(math.ceil(sum(window)/len(window)))

        for j in a[-size:]:
            b.append(j)
        return b
    else:
        kernel=[1]*(size*2-1)
        for i in range(1,size*2):
            kernel[i-1]= math.exp(-(i-size)**2/(2*sigma**2))/(sigma*math.sqrt(2*math.pi))    
        b=scipy.signal.convolve(a[size-1:-size+1],kernel)
        b[:size+1]=a[:size+1]
        b[-size-1:]=a[-size-1:]
        
        #plt.plot(range(50,50+len(b)),b, marker='.')
        return b



#def filter_gaussian(a, size, sigma):
if __name__=='__main__':

    # parameters for filter
    #flt_type='median'
    flt_type=sys.argv[3]
    #flt_type='mean'
    #flt_type='No'
    size=int(sys.argv[4])

    nb_video=sys.argv[1]
    direction=sys.argv[2]

    # read files
    files=os.listdir('testVedios/test'+nb_video+'/') 
    print(direction[1:])
        
    for i in files:
        if (len(re.findall('joints_3DKinect_.'+direction[1:]+'2', i))!=0):
            filecm=i
    print(filecm)   
    k=pd.DataFrame(pd.read_csv('testVedios/test'+nb_video+'/'+filecm))

    # show original ankle dis            
    fig1=plt.figure()
    ax1=fig1.add_subplot(111)
    ax1.plot(k['frames'], k['z_lak'], marker='.', color='b', lw=1.8)
    ax1.plot(k['frames'], k['z_rak'], marker='.', color='r', lw=1.8)

    # show corrected ankle dis
    print('-----correct1 for ak-----')
    correct1(k['z_lak'], k['bad_frame'], 'ak', 3)
    print('---------')
    correct1(k['z_rak'], k['bad_frame'], 'ak', 3)
    ax1.plot(k['frames'], k['z_lak'], marker='.', color='b', lw=1.5)
    ax1.plot(k['frames'], k['z_rak'], marker='.', color='r', lw=1.5)
    print('-----correct2 for ak-----')
    correct2(k['z_lak'], k['bad_frame'], err_type=11)
    correct2(k['z_rak'], k['bad_frame'], err_type=10)
    print('-----filter for ak-----')
    k['z_rak']=filter(list(k['z_rak']),size, flt_type)
    k['z_lak']=filter(list(k['z_lak']),size, flt_type)
    k['x_rak']=filter(list(k['x_rak']),size, flt_type)
    k['x_lak']=filter(list(k['x_lak']),size, flt_type)
    k['y_rak']=filter(list(k['y_rak']),size, flt_type)
    k['y_lak']=filter(list(k['y_lak']),size, flt_type)
    
    ax1.plot(k['frames'], k['z_lak'], marker='.', color='#87CEFA', lw=1.2)
    ax1.plot(k['frames'], k['z_rak'], marker='.', color='#FFC0CB', lw=1.2)
    ax1.set_ylabel('z of ak_kinect')
    ax1.set_xlabel('frame')
    ax1.set_title('Correction for ak')

    # show original as dis            
    fig2=plt.figure()
    ax4=fig2.add_subplot(111)
    ax4.plot(k['frames'], k['z_las'], marker='.', color='b', lw=1.8)
    ax4.plot(k['frames'], k['z_ras'], marker='.', color='r', lw=1.8)

    # show corrected as dis
    print('-----correct1 for as-----')
    correct1(k['z_las'], k['bad_frame'], 'ak', 1)
    print('----------')
    correct1(k['z_ras'], k['bad_frame'], 'ak', 1)
    print('-----correct2 for as-----')
    correct2(k['z_las'], k['bad_frame'], err_type=21)
    correct2(k['z_ras'], k['bad_frame'], err_type=20)
    print('-----filter for as-----')
    k['z_ras']=filter(list(k['z_ras']),size, flt_type)
    k['z_las']=filter(list(k['z_las']),size, flt_type)
    k['x_ras']=filter(list(k['x_ras']),size, flt_type)
    k['x_las']=filter(list(k['x_las']),size, flt_type)
    k['y_ras']=filter(list(k['y_ras']),size, flt_type)
    k['y_las']=filter(list(k['y_las']),size, flt_type)
    
    ax4.plot(k['frames'], k['z_las'], marker='.', color='#87CEFA', lw=1.2)
    ax4.plot(k['frames'], k['z_ras'], marker='.', color='#FFC0CB', lw=1.2)
    ax4.set_ylabel('z of as_kinect')
    ax4.set_xlabel('frame')
    ax4.set_title('Correction for as')

    # show original kn dis            
    fig3=plt.figure()
    ax5=fig3.add_subplot(111)
    ax5.plot(k['frames'], k['z_lkn'], marker='.', color='b', lw=1.8)
    ax5.plot(k['frames'], k['z_rkn'], marker='.', color='r', lw=1.8)

    # show corrected as dis
    print('-----correct1 for kn-----')
    correct1(k['z_lkn'], k['bad_frame'], 'kn', 3)
    print('----------')
    correct1(k['z_rkn'], k['bad_frame'], 'kn', 3)
    print('-----filter for kn-----')
    k['z_rkn']=filter(list(k['z_rkn']),size, flt_type)
    k['z_lkn']=filter(list(k['z_lkn']),size, flt_type)
    k['x_rkn']=filter(list(k['x_rkn']),size, flt_type)
    k['x_lkn']=filter(list(k['x_lkn']),size, flt_type)
    k['y_rkn']=filter(list(k['y_rkn']),size, flt_type)
    k['y_lkn']=filter(list(k['y_lkn']),size, flt_type)
    
    ax5.plot(k['frames'], k['z_lkn'], marker='.', color='#87CEFA', lw=1.2)
    ax5.plot(k['frames'], k['z_rkn'], marker='.', color='#FFC0CB', lw=1.2)
    ax5.set_title('z\' of KN_kinect')
    ax5.set_ylabel('z of kn_kinect')
    ax5.set_xlabel('frame')
    ax5.set_title('Correction for kn')

    # show corrected knee angles
    for i in range(len(k['frames'])):
        k['kangle_l'][i]=180-tools.angle((k['x_lak'][i],k['y_lak'][i],k['z_lak'][i]),(k['x_lkn'][i],k['y_lkn'][i],k['z_lkn'][i]),(k['x_las'][i],k['y_las'][i],k['z_las'][i]), False)
        k['kangle_r'][i]=180-tools.angle((k['x_rak'][i],k['y_rak'][i],k['z_rak'][i]),(k['x_rkn'][i],k['y_rkn'][i],k['z_rkn'][i]),(k['x_ras'][i],k['y_ras'][i],k['z_ras'][i]), False) 
    fig4=plt.figure()
    ax2=fig4.add_subplot(211)
    ax2.plot(k['frames'], k['kangle_l'])
    ax3=fig4.add_subplot(212)
    ax3.plot(k['frames'], k['kangle_r'], color='r')
    ax2.set_title('Corrected 3D Kinect Knee Angle (filter: '+flt_type+' size: '+str(size)+')') 
    ax2.set_ylabel('Angle_left')
    ax3.set_ylabel('Angle_right')

    ax2.set_xlabel('frame')
    ax3.set_xlabel('frame')
    #ax3.set_title('Right Knee angle') 
    
    # show corrected ankle x y and z
    fig5=plt.figure()
    ax6=fig5.add_subplot(221)
    ax6.plot(k['frames'], k['x_lak'], color='b')
    ax6.plot(k['frames'], k['x_rak'], color='r')
    ax6.set_title('Variation de \'x\' de la cheville')
    ax6.set_xlabel('frame')
    ax6.set_ylabel('Left(blue)  Right(red)')
    
    ax7=fig5.add_subplot(222)
    ax7.plot(k['frames'], k['y_lak'], color='b')
    ax7.plot(k['frames'], k['y_rak'], color='r')
    ax7.set_title('Variation de \'y\' de la cheville')
    ax7.set_xlabel('frame')
    ax7.set_ylabel('Left(blue)  Right(red)')
    
    ax8=fig5.add_subplot(223)
    ax8.plot(k['frames'], k['z_lak'], color='b')
    ax8.plot(k['frames'], k['z_rak'], color='r')
    ax8.set_title('Variation de \'z\' de la cheville')
    ax8.set_xlabel('frame')
    ax8.set_ylabel('Left(blue)  Right(red)')
     
    ax9=fig5.add_subplot(224)
    ax9.plot(k['frames'], k['kangle_l'], color='b')
    ax9.plot(k['frames'], k['kangle_r'], color='r')
    ax9.set_xlabel('frame')
    ax9.set_ylabel('Left(blue)  Right(red)')
    ax9.set_title('Variation d\'angle de genou')
    
    plt.show()


    # save new file
    number=(re.search('[0-9]+',filecm).group(0)) 
    for c in k.keys():
        if len(re.findall('Unnamed',c))!=0:
            k.drop([c],axis=1,inplace=True)
    if direction=='back':
        k.to_csv('testVedios'+'/test'+nb_video+'/'+number+'_LCR-NET_joints_3DKinect_back3.csv',encoding='gbk')
    else:
        k.to_csv('testVedios'+'/test'+nb_video+'/'+number+'_LCR-NET_joints_3DKinect_front.csv',encoding='gbk')
    print(number,': File is saved!')
