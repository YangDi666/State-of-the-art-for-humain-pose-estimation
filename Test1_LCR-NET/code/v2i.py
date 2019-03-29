
import cv2
import os
import matplotlib.pylab as plt
import numpy as np
import tools

frame=107
cap= cv2.VideoCapture('test1/1536334071006611046C.mp4')  


while (cap.isOpened()):
	cap.set(cv2.CAP_PROP_POS_FRAMES, frame)  # 设置帧数标记
	ret, im = cap.read()  # read方法返回一个布尔值和一个视频帧
	
	cv2.imwrite("test1/" + str(frame) + "C.jpg", im)  # 保存图片
	frame += 1000 # 设置帧数
	if not ret:
		break
cap.release()

