import tqdm
from create_annotations import *
from PIL import Image
import os
import json
import glob
import pandas as pd
'''
coco format json으로 변경하는 파일입니다. 
'''

# category name, image 개수, image annotation 개수

# Label ids of the dataset
category_ids = {}
train_anno_path = '/opt/ml/final_project/data/anno/train' # 바게뜨빵, 바게뜨빵 json, 바나나, ...

category_list = list(filter(lambda x : x.endswith('json'), os.listdir(train_anno_path))) # train json 폴더의 base path가 저장
# train_image_path = os.path.join(train_path, category_list)
# train_label_path = os.path.join(train_path, list(filter(lambda x:'json' in x, os.listdir(train_path))))
category_list = list(set(category_list)) # 가나다 순 정렬
category_list.sort()

category_name_list = []
image_count_list =[]
image_annotation_count_list =[]
anno_dict = {'category_name':[], 'image_count': [], 'image_annotation_count':[] }




for idx, category in tqdm.tqdm(enumerate(category_list)):
    count = 0
    total_path = glob.glob(os.path.join(train_anno_path, category, '*.json'))
    image_count = len(total_path)
    image_annotation_count = 0
    for json_path in total_path:
        with open(json_path,'r') as json_file:
            json_label = json.load(json_file)
        image_annotation_count += len(json_label)

    category_name = json_label[0]['Name'] # samgyetang

    anno_dict['category_name'].append(category_name)
    anno_dict['image_count'].append(image_count)# category별 이미지 개수
    anno_dict['image_annotation_count'].append(image_annotation_count)# category별 annotation 개수

df = pd.DataFrame(anno_dict)
print(df)
df.to_csv('./annotation_korea.csv')

print(category_ids)