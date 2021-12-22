import tqdm
from create_annotations import *
from PIL import Image
import os
import json
import glob
import argparse
import pandas as pd
'''
영어 카테고리 이름과 한국어 카테고리 이름이 짝지어진 csv파일을 만드는 코드입니다.
'''

# category name, image 개수, image annotation 개수

# Label ids of the dataset
category_ids = {}
train_path = 'C:/Users/charl/projects/data/Validation' # 바게뜨빵, 바게뜨빵 json, 바나나, ...

category_list = list(filter(lambda x : x.endswith('json'), os.listdir(train_path))) # train json 폴더의 base path가 저장
category_list = list(category_list) # 가나다 순 정렬
category_list.sort()

# Label ids of the dataset
anno_dict = {'category_name':[], 'korean_name':[]} # to csv
category_ids = {}

for idx, category in tqdm.tqdm(enumerate(category_list)):
    count = 0
    total_path = glob.glob(os.path.join(train_path, category, '*.json'))
    image_annotation_count = 0
    category = ' '.join(category.split()[:-1])
    category_ids[category] = idx
    for json_path in total_path:
        with open(json_path,'r') as json_file:
            json_label = json.load(json_file)
        break

    category_name = json_label[0]['Name'] # samgyetang

    anno_dict['category_name'].append(category_name)
    anno_dict['korean_name'].append(category)
    

df = pd.DataFrame(anno_dict)
print(df)
df.to_csv('./annotation_korea.csv')

print(category_ids)