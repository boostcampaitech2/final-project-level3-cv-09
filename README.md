# 재활용 품목 분류를 위한 Sementic Segmentation in Bostcamp

## 💻 하나둘셋Net()

### 😎 Members

---

|                                     [공은찬](https://github.com/Chanchan2)                                      |                                       [곽민구](https://github.com/deokgu)                                       |                                      [김준섭](https://github.com/Aweseop)                                       |                                     [김진용](https://github.com/Kim-jy0819)                                     |                                       [심용철](https://github.com/ShimYC)                                       |                               [오재석](https://github.com/dmole20)                                |                                     [최현진](https://github.com/hyeonjini)                                      |
| :-------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: |
| ![image](https://user-images.githubusercontent.com/13193985/140293018-d3a12aa8-485b-4c97-b6ab-a9dc78a81c99.jpg) | ![image](https://user-images.githubusercontent.com/35412566/138591171-7b883dcd-7b83-492e-a251-9eb2960d6e62.png) | ![image](https://user-images.githubusercontent.com/35412566/138591221-5c2b12cc-c2db-4679-892f-a0aa034cdf77.png) | ![image](https://user-images.githubusercontent.com/63527907/140073918-839313ff-76f0-4bd1-a1da-2b68880c8f43.png) | ![image](https://github.com/ShimYC/ShimYC.github.io/blob/main/images/KakaoTalk_20211104_233517667.jpg?raw=true) |                ![image](https://avatars.githubusercontent.com/u/52789601?s=40&v=4)                | ![image](https://github.com/hyeonjini.png) |
| [**Notion**](https://flint-failing-3c9.notion.site/006b28bf92104405834e3fb3ef1fdc99)                                                                                                             |                                [**TIL**](https://github.com/deokgu/deokgu/wiki)                                 |   [**Git**](https://github.com/Aweseop)                                                                                                              | [**Blog**](https://near-prawn-9c5.notion.site/Naver-Boost-Camp-AI-Tech-2-2e4303f8bd2e4f36be8916d04cbd123a)                                                                                                                | [**Notion**](https://bubbly-cost-eda.notion.site/AI-boostcamp-memo-2f012708dd2645bb9962679ad51c6490)                                                                                                                | [**TIL**](https://fair-dahlia-cc2.notion.site/BoostCamp-AI-Tech-48bd706756aa49e0b74ca2d2ffda962a) |[**Devlog**](https://velog.io/@choihj94)                                                                                                                 |

---

## 🔎 Competition Overview

<br>

![image](https://user-images.githubusercontent.com/35412566/139359859-ea1469d8-8bd9-41f3-b09e-4b190ab795db.png)

##### 잘 분리 배출 된 쓰레기는 자원으로서 가치를 인정받아 재활용되지만, 잘못 분리배출 되면 그대로 폐기물로 분류되어 매립 또는 소각되기 됩니다.

##### 따라서 우리는 사진에서 쓰레기를 Segmentation하는 모델을 만들어 이러한 문제점을 해결해보고자 합니다. 문제 해경을 위한 데이터셋으로는 배경, 일반 쓰레기, 플라스틱, 종이, 유리 등 11종류의 쓰레기가 찍힌 사진 데이터셋이 제공됩니다.

##### 여러분에 의해 만들어진 우수한 성능의 모델은 쓰레기장에 설치되어 정확한 분리수거를 돕거나, 어린아이들의 분리수거 교육 등에 사용될 수 있을 것입니다.

---

## 🎉 수행결과 best score?

### ✨ 리더보드(대회 진행): **11위** mIoU : 0.757

### 🎊 리더보드(최종): **14위** mIoU : 0.706

<br>

---

## 🎮 Requirements

- Linux version 4.4.0-59-generic
- Python >= 3.8.5
- PyTorch >= 1.7.1
- conda >= 4.9.2
- tensorboard >= 2.4.1

### ⌨ Hardware

- CPU: Intel(R) Xeon(R) Gold 5220 CPU @ 2.20GHz
- GPU: Tesla V100-SXM2-32GB
  <br>

## 🔍 Reference

- [MMsegmentation](https://github.com/open-mmlab/mmsegmentation)
- [RAdam](https://github.com/LiyuanLucasLiu/RAdam/blob/master/radam/radam.py)
- [Copy-Paste](https://arxiv.org/pdf/2012.07177v1.pdf)
  <br>
  
## 📏 역할
| 팀구성  | 역할 |
| :---:   | :---:|
| 공은찬_T2009| Custom loss, Optimizer 적용|
| 곽민구_T2255| Optimizer, Loss, Scheduler Test 진행 |
| 김준섭_T2056| Segmentation Multi-label Stratified K-fold 구성|
| 김진용_T2063| Copy paste 데이터 셋 제작|
| 심용철_T2122| Model 탐색, Resize 및 weighted loss 실효성 검증|
| 오재석_T2133| Stratified K-fold 데이터셋 코드 틀 작성|
| 최현진_T2234| Baseline Code 작성, Pseudo Labeling, Oversampling|


# 🔨 수행 과정

---

## 🔑 Validation Dataset 구성
- Segmentation task에서 데이터를 reasonable하게 train/val dataset을 나누기 위함
- 아래와 같이 각 이미지마다 3가지 label을 정의 후 Multi-label Stratified K-Fold로 데이터를 나눔
```
 수가 적은 Class를 최대한 포함하기 위해 이미지마다 가장 적은 수에 해당하는 클래스를 이미지의 클래스로 정의
 이미지당 Class의 수
 이미지당 Annotation의 수
````
 ![image](https://user-images.githubusercontent.com/35412566/140275405-f42a0fd4-37ae-41be-986f-39ee5a6847c9.png)


<br>

---

## 🔑 Oversampling
![image](https://user-images.githubusercontent.com/35412566/140275754-58e33ecd-8e5b-4581-8655-6f153ed11412.png)
<br>

![image](https://user-images.githubusercontent.com/35412566/140275802-3f83cd8e-9854-422d-86b3-c58c2051af5a.png)

<br>

---

## 🔑 Pseudo Labeling
- 가장 성능이 좋은 모델의 inference 결과로 학습 데이터를 만들고 재학습
- Segmentation task 특성으로 점수 크게 향상(0.727 -> 0.75)

<br>

---
## 🔑 DenseCRF
- Dense CRF 기법을 적용해 boundary 좀 더 뚜렷하게 반영, 단일 객체에서 성능 향상 기대
![image](https://user-images.githubusercontent.com/35412566/140275995-7967b185-5dd8-4e74-b36c-0558408a436c.png)

<br>

---

## 📂 Archive contents

```
baseline/
├── train.py # main
├── trainer.py
├── dataset.py
├── test.py
├── utils.py
└── models/ # train model package
└── loss/ # loss metric package
└── scheduler/ # scheduler package
└── model
  └── exp1/ # model file will save here
```

```
util/
├── oversampling.py
└── pseudo_labeling.py
```

```
copy_paste/
├─ check_copy_paste.ipynb
├─ copy_paste.py
├─ mask_convert_json.py
├─ get_coco_mask.py
├─ README.md
└─ requirements.txt
```

<br>

## 💎Copy Paste

<br>

### Augmentation Method:
1. Random Horizontal Flip
2. Large Scale Jittering
3. Copy-Paste
4. Large patch to Small patch
5. Small patch to Large patch
6. Random Flip

### Copy_paste Quick Start 

### 1. 쉘 스크립트를 사용하고자 한다면 해당 디렉토리에 들어가 다음 명령어를 입력한다.
```
./aug.sh
```
<br>

### 2. 명령어를 따로 입력하고자 한다면 다음과 같은 순서로 명령어를 입력한다.
#### 1. 모듈 설치하기
```
pip install -r requirements.txt
```

<br>

#### 2. 원본 이미지와 json 파일을 통해 segmentation mask 생성
```
python get_coco_mask.py  
--input_dir ../../input/data/ 
--split train_all
```

<br>

#### 3. 원본 이미지, 원본 mask, 랜덤 이미지, 랜덤 mask로부터 copy_paste
```
python copy_paste.py --input_dir ../../input/data/ --output_dir ../../input/data/ 
--patch ["Paper pack", "Battery", "Plastic", 'Clothing',"Glass" ]
--remove_patch ["Paper", "Plastic bag"]
--json_path train.json
--lsj True
--lsj_max 2
--lsj_min 0.2
--aug_num 1500
--extract_patch True
```

![image](https://user-images.githubusercontent.com/63527907/139034387-1ec9d9c8-3dcd-4859-9f8a-5ead0fe54f40.png)

<br>

#### 4. mask로부터 json파일로 변환
```
python mask_coco_mask.py
--main_json train.json
--mode add
```

#### 5. 결과

![image](https://user-images.githubusercontent.com/63527907/139034173-370fd30e-42dc-40c3-afe1-00ed559fbb2a.png)
---

## 🛒 Train Test Quickstart
```
python train.py \
--model UPlusPlus_Efficient_b5 \
--epochs 200 \
--loss FocalLoss \
--val_json kfold_0_val.json \
--train_json kfold_0_train.json \
--train_augmentation CustomTrainAugmentation \
--batch_size 5
```
```
python test.py python test.py --model_dir model/exp --model_name epoch10.pth --augmentation TestAugmentation
```
- reference here `exmple/`

- 파일 구조를 다음과 같이 합니다.

![image](https://user-images.githubusercontent.com/63527907/142895213-49b5bcc6-7ba3-4583-a28e-b251676c45bc.png)

```
python convert_coco_data.py
```
