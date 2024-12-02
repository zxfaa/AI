# 導入相關套件
import cv2  # OpenCV用於影像處理的函式庫
import pandas as pd  # Pandas用於資料處理和分析的函式庫
from ultralytics import YOLO  # Ultralytics的YOLO物件偵測模型
from tracker import *  # 自定義的物件追蹤模組
import os

# 設定當前目錄為工作目錄
os.chdir(os.path.dirname(__file__))

# 初始化YOLO模型，使用提供的預訓練權重檔案 'yolov8n.pt'
model = YOLO('yolov8n.pt')

# 定義滑鼠事件回調函數，用於在滑鼠移動時捕捉RGB值
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

# 創建顯示RGB值的視窗並設定滑鼠回調函數
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# 打開一個視訊檔案來捕捉影格
cap = cv2.VideoCapture('veh2.mp4')

# 從 'coco.txt' 文件中讀取類別名稱
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

# 初始化計數和物件追蹤器
count = 0
tracker = Tracker()

# 定義兩條檢測線和偏移量等相關變數
cy1 = 322
cy2 = 368
offset = 6

# 主迴圈用於處理視訊影格
while True:    
    ret, frame = cap.read()
    if not ret:
        break
    count += 1

    # 跳過一些影格以加快處理速度
    if count % 3 != 0:
        continue

    # 將影格調整大小以保持一致性
    frame = cv2.resize(frame, (1020, 500))

    # 使用YOLO模型預測影格中的物件
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
#    print(px)
    list = []
             
    for index, row in px.iterrows():
#        print(row)
 
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'car' in c:
            list.append([x1, y1, x2, y2])
    bbox_id = tracker.update(list)
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = int(x3 + x4) // 2
        cy = int(y3 + y4) // 2
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
        cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
           

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
