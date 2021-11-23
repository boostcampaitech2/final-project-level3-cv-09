import tqdm
from create_annotations import *
from PIL import Image
import os
import json
import glob
'''
coco format json으로 변경하는 파일입니다. 
'''



# Label ids of the dataset
category_ids = {}
train_path = 'C:/Users/charl/projects/make_coco_format/data/Training' # 바게뜨빵, 바게뜨빵 json, 바나나, ...
category_list = list(filter(lambda x:'json' not in x ,os.listdir(train_path)))
# train_image_path = os.path.join(train_path, category_list)
# train_label_path = os.path.join(train_path, list(filter(lambda x:'json' in x, os.listdir(train_path))))
category_list.sort() # 가나다 순 정렬
for idx, category in enumerate(category_list):
    category_ids[category] = idx


# Get "images" and "annotations" info 
def images_annotations_info(train_path):
    # This id will be automatically increased as we go
    annotation_id = 0
    image_id = 0
    annotations = []
    images = []
    for category in category_list:
        for image in tqdm.tqdm(glob.glob(os.path.join(train_path, category, "*.jpg"))):
            # Load each json file along with image
            file_name = os.path.join(category, os.path.basename(image)) #'바나나/A020112XX_00866.jpg'
            try: 
                with open(image.replace('.jpg','.json').replace(f'{category}',f'{category} json'),'r') as json_file:
                    json_label = json.load(json_file)
            except:
                continue

            # Open the image and (to be sure) we convert it to RGB
            image_open = Image.open(image).convert("RGB")
            image_w, image_h = image_open.size
            
            # "images" info 
            image_annotation = create_image_annotation(file_name, image_w, image_h, image_id)
            images.append(image_annotation)
            
            # annotation info
            for ann in json_label:
                x, y = map(float, ann['Point(x,y)'].split(','))
                w, h = float(ann['W']), float(ann['H'])
                box_mid_x, box_mid_y, box_w, box_h = image_w*x, image_h*y, image_w*w, image_h*h
                bbox = [box_mid_x, box_mid_y, box_w, box_h]
                annotation = create_annotation_format(bbox, image_id, category_ids[category], annotation_id)
                annotations.append(annotation)
                annotation_id += 1
            image_id += 1

    return images, annotations, annotation_id

if __name__ == "__main__":

    # Get the standard COCO JSON format
    coco_format = get_coco_json_format()
    
    
    # Create category section
    coco_format["categories"] = create_category_annotation(category_ids)

    # Create images and annotations sections
    coco_format["images"], coco_format["annotations"], annotation_cnt = images_annotations_info(train_path)

    with open("C:/Users/charl/projects/make_coco_format/data/train.json","w") as outfile:
        json.dump(coco_format, outfile)
