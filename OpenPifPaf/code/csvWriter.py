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

for j in tqdm(range(17)):
  
    data={'frame':[], 'x2d_'+str(j+1):[], 'y2d_'+str(j+1):[]}
    for i in range(len(list_frames)):    
        data['frame'].append(i+1)
        if (list_frames[i]==[]):
            data['x2d_'+str(j+1)].append('No')
            data['y2d_'+str(j+1)].append('No')
        else:
            data['x2d_'+str(j+1)].append(list_frames[i][0]['pose2d'][j])
            data['y2d_'+str(j+1)].append(list_frames[i][0]['pose2d'][j+njts])
            
    data=pd.DataFrame(data)

    data.to_csv('testVideos'+'/test'+n+'/test'+n+'_PifPaf_point'+str(j+1)+'.csv',encoding='gbk')
