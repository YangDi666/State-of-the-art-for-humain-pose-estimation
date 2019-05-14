import cv2
import os
import re

def imgs2video(save_name, nb_video): 
    fps = 6 
    fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
    video_writer = cv2.VideoWriter(save_name, fourcc, fps, (641, 361)) # no glob, need number-index increasing 
    imgs=os.listdir('test'+nb_video+'/') 
    imgs.sort()
    for i in imgs: 
        print(re.findall('.*\.png',i))
        if len(re.findall('.*\.png',i))!=0:
            frame = cv2.imread('test'+nb_video+'/'+i) 
            video_writer.write(frame) 
            print('done')
    video_writer.release()
imgs2video('test2/test2.avi', '2')