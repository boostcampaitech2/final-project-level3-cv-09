import os
import json
import yaml
import glob
import tqdm
import argparse
import numpy as np

import warnings
warnings.filterwarnings(action='ignore')


def get_confuse_json(label_path) :
    text_list = os.listdir(label_path)
    len(text_list)
    json_data = {}

    for text in text_list :
        with open(os.path.join(label_path, text), 'r') as file :
            text_id = text.replace('.txt', '')
            json_data[text_id] = {}
            for line in file :
                cat, xmin, ymin, xmax, ymax, conf = line.split()
                xmin, ymin, xmax, ymax = map(str, map(lambda x: round(float(x), 2), [xmin, ymin, xmax, ymax]))
                anno_id = '/'.join([xmin, ymin, xmax, ymax])
                if anno_id not in json_data[text_id].keys() :
                    json_data[text_id][anno_id] = {}
                    json_data[text_id][anno_id]['gt_category_id'] = None
                    json_data[text_id][anno_id]['1st_category_id'] = [cat, float(conf)]
                    json_data[text_id][anno_id]['2nd_category_id'] = None
                    json_data[text_id][anno_id]['3rd_category_id'] = None
                    json_data[text_id][anno_id]['variance'] = 1
                
                else :
                    if json_data[text_id][anno_id]['2nd_category_id'] is None :
                        json_data[text_id][anno_id]['2nd_category_id'] = [cat, float(conf)]
                        dev_1 = json_data[text_id][anno_id]['1st_category_id'][1] - json_data[text_id][anno_id]['2nd_category_id'][1]
                        var = (dev_1)**2 / 2
                        json_data[text_id][anno_id]['variance'] = var
                    elif json_data[text_id][anno_id]['3rd_category_id'] is None :
                        json_data[text_id][anno_id]['3rd_category_id'] = [cat, float(conf)]
                        dev_1 = json_data[text_id][anno_id]['1st_category_id'][1] - json_data[text_id][anno_id]['2nd_category_id'][1]
                        dev_2 = json_data[text_id][anno_id]['1st_category_id'][1] - json_data[text_id][anno_id]['3rd_category_id'][1]
                        var = ((dev_1)**2 + (dev_2)**2) / 3
                        json_data[text_id][anno_id]['variance'] = var
                    else :
                        continue

    print(f'json length : {len(json_data.keys())}')
    return json_data

 
def edit_json(json_data, data_path) :
    img_list = list(json_data.keys())
    txt_path = glob.glob(os.path.join(data_path, '**', '*.txt'))

    # edit json data
    print('Json editing...')
    for img in tqdm.tqdm(img_list) :
        json_len = len(list(json_data[img].keys()))
        for file in txt_path :
            if img in file :
                with open(file, 'r') as f :
                    gt = f.readline().split(' ')[0]
                    for i in range(json_len) :
                        json_data[img][list(json_data[img].keys())[i]]['gt_category_id'] = gt
                break
    
    return json_data, img_list


def load_json(label_path, data_path, save_path, save_json_name) :
    if not os.path.exists(save_path) :
        os.makedirs(save_path)

    file_name = os.path.join(save_path, save_json_name)
    if os.path.exists(file_name) :
        print(f'Using already exist json file : {file_name}')
        print('\n')
        with open(file_name, 'r') as f :
            json_data = json.load(f)
            img_list = list(json_data.keys())

    else :
        json_data = get_confuse_json(label_path)
        json_data, img_list = edit_json(json_data, data_path)
        with open(file_name, 'w') as f :
            json.dump(json_data, f)
            print(f'Complete save json! : {file_name}')
            print('\n')

    return json_data, img_list


def get_confidence_variance(json_data, img_list, threshold) :
    confidence_variance = []
    for img in img_list :
        try :
            json_len = len(list(json_data[img].keys()))
            for i in range(json_len) :
                data = json_data[img][list(json_data[img].keys())[i]]
                if (data['2nd_category_id'] != None) and (data['variance'] <= threshold) :
                    confidence_variance.append(data)
        except :
            pass
    
    return confidence_variance


def get_gt_dict(confidence_variance) :
    category_list = ['1st_category_id', '2nd_category_id', '3rd_category_id']
    gt_list = [stat['gt_category_id'] for stat in confidence_variance if stat['gt_category_id'] != None]
    gt_list = list(set(gt_list))
    gt_dict = {gt : {} for gt in gt_list}

    for element in confidence_variance :
        gt = element['gt_category_id']
        if gt != None :
            id_list = [element[category][0] for category in category_list if element[category] != None]
            if (gt in id_list) and (len(list(set(id_list))) >= 2) : # 예측 카테고리안에 GT가 있고 유니크한 개수가 2개 이상인 경우만
                for category in category_list :
                    predict = element[category][0]
                    if predict != gt : # GT랑 예측값 다를 때 예측한 id, 개수, variance 뽑음.
                        if predict not in gt_dict[gt] :
                            gt_dict[gt][predict] = {'count' : 1, 'variance' : [element['variance']]}

                        else :
                            gt_dict[gt][predict]['count'] += 1
                            gt_dict[gt][predict]['variance'].append(element['variance'])
                        break

    return gt_dict


def get_variance_mean(gt_dict) :
    for key, value in gt_dict.items() :
        predict_list = gt_dict[key].keys()
        for predict in predict_list :
            gt_dict[key][predict]['variance'] = np.round(np.mean(gt_dict[key][predict]['variance']), 3)

    return gt_dict


def del_no_data(gt_dict) :
    for key in list(gt_dict.keys()) :
        if len(gt_dict[key]) == 0 :
            del gt_dict[key]

    return gt_dict


def get_top3(gt_dict) :
    for gt in gt_dict.keys() :
        gt_dict[gt] = sorted(gt_dict[gt].items(), key=lambda x: (x[1]['count'], -x[1]['variance']), reverse=True)[:3] # Top 3

    return gt_dict


def dict_cleansing(gt_dict) :
    gt_dict = del_no_data(gt_dict)
    gt_dict = get_variance_mean(gt_dict)
    gt_dict = get_top3(gt_dict)

    return gt_dict


def parse_name(yaml_path):
    assert os.path.isfile(yaml_path) 
    with open(yaml_path, 'r', encoding='utf-8') as f:
        names = yaml.load(f, Loader=yaml.FullLoader)['names']
        food_names = {str(id):name for id, name in enumerate(names)}

        return food_names


def show_confused_class(food_name, gt_dict, class_id) :
    try :
        class_id = str(class_id)
        if class_id == 'all' :
            class_id = list(gt_dict.keys())
        else :
            class_id = [class_id]
            
        for id in class_id :
            print(f'Confused class for {id} ({food_name[id]})')
            for i, element in enumerate(gt_dict[id]) :
                print(f'Top {i+1} - Id : {element[0]} ({food_name[element[0]]}), Count : {element[1]["count"]}, Variance : {element[1]["variance"]}')
            print('\n')

    except :
        if class_id[0] not in list(gt_dict.keys()) :
            raise ValueError(f'There is no result about {class_id[0]}')

        else :
            pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--threshold', type=int, default=0.05, help='variance threshold')
    parser.add_argument('--class_id', type=str, default='all', help='you can also enter a specific class id.')
    parser.add_argument('--label_path', type=str, default='/opt/ml/final/yolov5/runs/val/exp6/labels', help='you should execute val.py with --save-txt, --save-conf option')
    parser.add_argument('--data_path', type=str, default='/opt/ml/final/datasets/val', help='dataset path')
    parser.add_argument('--save_path', type=str, default='/opt/ml/final/yolov5/custom_metric', help='json save path')
    parser.add_argument('--save_json_name', type=str, default='output.json', help='json save name')
    parser.add_argument('--yaml_path', type=str, default='/opt/ml/final/yolov5/data/coco.yaml', help='coco yaml path')

    args = parser.parse_args()
    return args


def main(args) :
    json_data, img_list = load_json(args.label_path, args.data_path, args.save_path, args.save_json_name)
    confidence_variance = get_confidence_variance(json_data, img_list, threshold=args.threshold)
    print(confidence_variance)
    gt_dict = get_gt_dict(confidence_variance)
    gt_dict = dict_cleansing(gt_dict)
    food_name = parse_name(args.yaml_path)
    show_confused_class(food_name, gt_dict, args.class_id)


if __name__ == '__main__' :
    args = parse_args()
    main(args)
