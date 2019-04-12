import json
import pandas as pd
from tqdm import tqdm
import sys
import re

n=sys.argv[1]
name=sys.argv[2]
#name=re.findall('/[1-9]+.*_',name)[0][1:-1]
print(name)
with open('testVideos'+'/test'+n+'/'+name+'.json') as json_data:
    d = json.load(json_data)

njts = d['njts']
list_frames=d['frames']

for j in tqdm(range(njts+1)):
    if(j<=njts-1):
        data={'frame':[], 'x2d_'+str(j+1):[], 'y2d_'+str(j+1):[],'x3d_'+str(j+1):[], 'y3d_'+str(j+1):[],'z3d_'+str(j+1):[]}
        for i in range(len(list_frames)):    
            data['frame'].append(i+1)
            if (list_frames[i]==[]):
                data['x2d_'+str(j+1)].append('No')
                data['y2d_'+str(j+1)].append('No')
                data['x3d_'+str(j+1)].append('No')
                data['y3d_'+str(j+1)].append('No')
                data['z3d_'+str(j+1)].append('No')
            else:
                data['x2d_'+str(j+1)].append(list_frames[i][0]['pose2d'][j])
                data['y2d_'+str(j+1)].append(list_frames[i][0]['pose2d'][j+njts])
                
                data['x3d_'+str(j+1)].append(list_frames[i][0]['pose3d'][j])
                data['y3d_'+str(j+1)].append(list_frames[i][0]['pose3d'][j+njts])
                data['z3d_'+str(j+1)].append(list_frames[i][0]['pose3d'][j+2*njts])

        data=pd.DataFrame(data)

        data.to_csv('testVideos'+'/test'+n+'/test'+n+'_OpenPose_point'+str(j+1)+'.csv',encoding='gbk')

    else:
        data={'frame':[], 'angle_left':[], 'angle_right':[]}
        for i in range(len(list_frames)):    
            data['frame'].append(i+1)
            if (list_frames[i]==[]):
                data['angle_left'].append('NO')
                data['angle_right'].append('NO')
            else:
                data['angle_left'].append(list_frames[i][0]['angle_left'])
                data['angle_right'].append(list_frames[i][0]['angle_right'])
        data=pd.DataFrame(data)

        data.to_csv('testVideos'+'/test'+n+'/test'+n+'_OpenPose_angles.csv',encoding='gbk')
   
