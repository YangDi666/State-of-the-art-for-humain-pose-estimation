import json
import os
import sys
import tools

nb_video=sys.argv[1]
if len(sys.argv)!=2:
    print('usage : python3 jsonParsing.py nb_videos')
    sys.exit(1)
files=os.listdir('testVideos/test'+nb_video+'/output/') 
files.sort()
imagename=files[0][:20]
jsondata={'K': 10, 'njts': 18, 'frames': []}

for i in files:

    with open('testVideos/test'+nb_video+'/output/'+i) as json_data:
        d = json.load(json_data)
    people=[]
    for j in d['people']:
      
        # detect only the middle person
        k=0
        n=0       
        while(k==0 and n<18):
            if(not (j['pose_keypoints'][3*n]<200 and j['pose_keypoints'][3*n]>10 and j['pose_keypoints'][3*n+1]<895 and j['pose_keypoints'][3*n+1]>280)):
                if(not (j['pose_keypoints'][3*n]<1950 and j['pose_keypoints'][3*n]>1600 and j['pose_keypoints'][3*n+1]<895 and j['pose_keypoints'][3*n+1]>300)):
                    if(not (j['pose_keypoints'][3*n]==0 and j['pose_keypoints'][3*n+1]==0)):

                        det={'cumscore': 0, 'pose2d': [], 'pose3d': [], 'angle_left': 0, 'angle_right': 0}
                        for k in range(18):
                            det['pose2d'].append(j['pose_keypoints'][3*k])
                            det['pose3d'].append(j['pose_keypoints'][3*k])
                        for k in range(18):
                            det['pose2d'].append(j['pose_keypoints'][3*k+1])
                            det['pose3d'].append(j['pose_keypoints'][3*k+1])
                        for k in range(18):
                            det['pose3d'].append(j['pose_keypoints'][3*k+2])
                        det['angle_left']=tools.angle(tools.get_pos(det,18,12),tools.get_pos(det,18,13),tools.get_pos(det,18,14))
                        det['angle_right']=tools.angle(tools.get_pos(det,18,9),tools.get_pos(det,18,10),tools.get_pos(det,18,11))
                        people.append(det)
                        k=1
                    else:
                        n+=1
                else:
                    k=1
            else:
                k=1
        '''
        det={'cumscore': 0, 'pose2d': [], 'pose3d': [], 'angle_left': 0, 'angle_right': 0}
        for k in range(18):
            det['pose2d'].append(j['pose_keypoints'][3*k])
            det['pose3d'].append(j['pose_keypoints'][3*k])
        for k in range(18):
            det['pose2d'].append(j['pose_keypoints'][3*k+1])
            det['pose3d'].append(j['pose_keypoints'][3*k+1])
        for k in range(18):
            det['pose3d'].append(j['pose_keypoints'][3*k+2])
        det['angle_left']=tools.angle(tools.get_pos(det,18,12),tools.get_pos(det,18,13),tools.get_pos(det,18,14))
        det['angle_right']=tools.angle(tools.get_pos(det,18,9),tools.get_pos(det,18,10),tools.get_pos(det,18,11))
        people.append(det)
        '''

    jsondata['frames'].append(people)
    print(len(people))
    if(len(people)>=2):
        print(people)
#print(tools.get_pos(jsondata['frames'][105][0],18,10))
#print(tools.get_pos(jsondata['frames'][105][0],18,9),tools.get_pos(jsondata['frames'][105][0],18,10),tools.get_pos(jsondata['frames'][105][0],18,11))
 
with open('testVideos/test'+nb_video+'/'+imagename+'.json', 'w') as outfile:
        json.dump(jsondata, outfile)

sys.exit(1) 