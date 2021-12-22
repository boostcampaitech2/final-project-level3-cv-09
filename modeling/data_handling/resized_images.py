import tqdm
from PIL import Image
import os
import glob
import argparse
import numpy as np
'''
n개의 resized 이미지를 추출하는 프로그램입니다.
'''



# Get "images" and "annotations" info 
def choose_n_resized_images(args):
    
    train_path = args.train_dir # 순두부찌개, 순살찜닭, 스테이크 ...  or ./data/Validation
    save_path = args.save_dir # resized_Training
    # make save path
    

    category_list = os.listdir(train_path) # 순두부찌개, 순살찜닭, 스테이크 ...
    category_list.sort() # 가나다 순 정렬

    for category in category_list:
        total_paths = glob.glob(os.path.join(train_path, category, "*.jpg"))
        if len(total_paths) > args.number:
            total_paths = np.random.choice(total_paths, args.number, replace=False)
        os.makedirs(os.path.join(save_path,category), exist_ok=True)

        for image in tqdm.tqdm(total_paths):
            # Load each json file along with image
            # Open the image and (to be sure) we convert it to RGB
            image_open = Image.open(image).convert('RGB')
            image_w, image_h = image_open.size
            image_open = image_open.resize((image_w//4, image_h//4))
            image_open.save(os.path.join(save_path, category, os.path.basename(image)))
    return        
        
    
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_dir", default="C:/Users/charl/projects/data/Training", type=str, help="Training/Validation") # train directory가 저장된 파일 경로를 바꿔주세요.
    parser.add_argument("--save_dir", default="C:/Users/charl/projects/data/resized_Training", type=str, help="resized_Training/resized_Validation") # 클래스당 1000장의 이미지를 저장할 경로를 지정해주세요.
    parser.add_argument("--number", default=1000, type=int, help="resized_Training/resized_Validation")

    return parser.parse_args()

if __name__ == "__main__":

    args = get_args()
    
    
    # Create images and annotations sections
    choose_n_resized_images(args)