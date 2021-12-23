# 간편한 식단관리 FoodLog

## 💻 하나둘셋Net()

### 😎 Members

---

|[공은찬](https://github.com/Chanchan2) |  [곽민구](https://github.com/deokgu94)|  [김준섭](https://github.com/Aweseop)  | [김진용](https://github.com/Kim-jy0819)|                  [심용철](https://github.com/ShimYC) |   [최현진](https://github.com/hyeonjini) |
| :-------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------: |
|![은찬님](https://user-images.githubusercontent.com/63527907/147105242-1506b2a9-83fb-4500-ae27-40a96786492f.jpg) |![민구님](https://user-images.githubusercontent.com/63527907/147105286-439b141d-4f0d-4702-aa58-5295c4f57549.png) | ![준섭님](https://user-images.githubusercontent.com/63527907/147105312-fd35fa13-fb8d-475c-a504-39711dc345af.jpg)  | ![진용님](https://user-images.githubusercontent.com/63527907/147105333-cfde0fec-7012-43fe-8f74-6298fed9fa42.png)| ![용철님](https://user-images.githubusercontent.com/63527907/147105350-98c2fcac-d13f-47ff-8897-f7167c431d72.jpg)|  ![현진님 (2)](https://user-images.githubusercontent.com/63527907/147105383-8314f309-d926-44e4-9833-1f16e700f4f5.jpg) |
| [**Notion**](https://flint-failing-3c9.notion.site/006b28bf92104405834e3fb3ef1fdc99)                                                                                                             |                                [**TIL**](https://github.com/deokgu/deokgu/wiki)                                 |   [**Git**](https://github.com/Aweseop)                                                                                                              | [**Blog**](https://near-prawn-9c5.notion.site/Naver-Boost-Camp-AI-Tech-2-2e4303f8bd2e4f36be8916d04cbd123a)                                                                                                                | [**Notion**](https://bubbly-cost-eda.notion.site/AI-boostcamp-memo-2f012708dd2645bb9962679ad51c6490)                                                                                                                |[**Devlog**](https://velog.io/@choihj94)                                                                                        |




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

- [Yolov5](https://github.com/open-mmlab/mmsegmentation)
- [DVC](https://dvc.org/)
- [Fast Api](https://fastapi.tiangolo.com/ko/)
- [데이터셋](https://aihub.or.kr/aidata/27674)
- [영양정보 DB](https://fatsecret.kr)

  <br>

## 📏 역할
| 팀구성  | 역할 |
| :---:   | :---|
| 공은찬_T2009| 데이터셋(Testset), custom metric, 모델링 |
| 곽민구_T2255| 데이터 버젼 관리(dvc), 모델링|
| 김준섭_T2056| Custom metric, 모델링
| 김진용_T2063| 데이터 가공, EDA |
| 심용철_T2122| EDA, Hyperparameter tuning, test dataset 수집 |
| 최현진_T2234| PM, 백엔드 개발, 안드로이드 개발, 영양정보 데이터 크롤링|
<br>

---
## 🛒 데이터 가공 및 학습데이터 생성

```python
# data_handling
cd modeling/data_handling

# 이미지 가로 세로 1/4씩 resize
python resized_images.py --train_dir {train_dir} --save_dir {save_dir}

# 음식명 한글, 영어 매칭
python make_Korean_English_category_csv.py 

# AI hub format을 coco format으로 변환
python hub2coco.py 

# coco format을 yolo format으로 변환
python coco2yolo.py --datasets COCO --img_path {img_path} --label {cocoformat.json} --img_type ".jpg"
```
<br>

---
## 🔍 EDA 
```python
# check_confuse_class 
# inference결과 헷갈리는 class 확인
python check_confuse_class.py --threshold {float} --class_id {int} --label_path {labels_dir} --data_path {dataset_dir} --save_path {save_dir} --save_json_name {save_name} --yaml_path {yaml_file_dir}
```
<br>

---

## 🔑 [모델 결과](https://wandb.ai/cv_09/yolov5?workspace=user-)

|![image](https://user-images.githubusercontent.com/35412566/147109464-9496e28f-dc4d-419a-807d-145f0dc7d2ca.png)| ![image](https://user-images.githubusercontent.com/35412566/147110369-16cf4951-af08-44ed-8afd-31249adb2fb9.png)|
|:---: | :---:|
<br>

## 🥐 프로젝트 구조
![image](https://user-images.githubusercontent.com/51802825/147062582-13f3d2c1-a563-4795-8636-d715cbe4be1f.png)

<br>

---
## 📱 안드로이드 앱 개발
![image](https://user-images.githubusercontent.com/51802825/147062982-46f57e48-47a5-49cf-aa60-3efc24a768f0.png)

<br>

---
## 🎨 사용자 피드백 모니터링
![image](https://user-images.githubusercontent.com/35412566/147100722-3b12634b-fb56-441d-888d-c1cf430b5b73.png)

---
## 🎁 배포
mysql run container
```
docker run --name mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABSE=food_db -d -p 3306:3306 mysql:5.7.12
```
backend image build & run container
```
cd server/backend
docker build . -t <tag> # docker image build
docker run --name foodlog-backend --link mysql -d -p 8000:8000 -v /app/images:/home/backend/images foodlog-backend
```
frontend image build & run contatiner
```
cd server/frontend
docker build . -t <tag> docker image build
docker run --name foodlog-frontend --link foodlog-backend -d -p 8502:8502 --volumes-from foodlog-backend foodlog-frontend
```
<br>

---

## 📂 Archive contents

```
modeling/
├── data_handling
|  |  annotation.csv
|  |  food.names
|  |  Format.py
|  |  coco2yolo.py
│  │  hub2coco_data.py
│  │  create_annotations.py
│  │  make_Korean_English_categroy_csv.py
│  └─ resized_images.py
├── eda
│  │  check_confuse_class.py
│  └─ make_total_label_count_csv.py
└── model
   └─ yolov5
```

```
server
│  docker-compose.yml
│
├─backend
│  │  best.pt
│  │  database.py
│  │  Dockerfile
│  │  main.py
│  │  nutrition.csv
│  │  requirements.txt
│  ├─dao
│  │  │  dao.py
│  │  └─ __init__.py
│  ├─model
│  │  │  model.py
│  │  │  schemas.py
│  │  │  service.py
│  │  └─ __init__.py
│  ├─predict
│  │  │  predict.py
│  │  └─ __init__.py
│  ├─service
│  │  │  service.py
│  │  └─ __init__.py
└─frontend
        Dockerfile
        main.py
        requirements.txt
```
<br>

---

## 실행 결과

![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/51802825/147072941-623a25d6-7214-43cf-9715-011c69b7eef1.gif)
<br>
---

