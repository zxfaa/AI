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
cy1 = 323
cy2 = 368
offset = 6
vh_down = {}  # 用於存儲下行車輛的字典，以車輛ID為鍵，Y坐標為值
counter = []  # 用於計算下行車輛數量的列表
vh_up = {}  # 用於存儲上行車輛的字典，以車輛ID為鍵，Y坐標為值
counter1 = []  # 用於計算上行車輛數量的列表

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
    # a = results[0].boxes.boxes
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    # print(px)
    list = []

    # 迭代處理每一行(row)，即每個偵測到的物件
    for index, row in px.iterrows():
        # 提取物件的座標和類別
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        
        # 如果該物件是車輛，將其座標加入清單
        if 'car' in c:
            list.append([x1, y1, x2, y2])
    
    # 使用物件追蹤器更新當前影格的物件位置
    bbox_id = tracker.update(list)
    
    # 迭代處理每個被追蹤的物件
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = int(x3 + x4) // 2
        cy = int(y3 + y4) // 2
        
        # 畫圓和文字，標識追蹤到的物件
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
        cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

        # ------------Down----------------
        if cy1 < (cy + offset) and cy1 > (cy - offset):
            vh_down[id] = cy
        
        # 如果車輛ID在下行車輛的字典中
        if id in vh_down:
            if cy2 < (cy + offset) and cy2 > (cy - offset):
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                cv2.putText(frame, str(id), (cx, cy),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                # 如果車輛ID不在計數列表中，將其添加進去
                if counter.count(id) == 0:
                    counter.append(id)
                    
        # -------------UP------------------
        if cy2 < (cy + offset) and cy2 > (cy - offset):
            vh_up[id] = cy
        
        # 如果車輛ID在上行車輛的字典中
        if id in vh_up:
            if cy1 < (cy + offset) and cy1 > (cy - offset):
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                cv2.putText(frame, str(id), (cx, cy),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                # 如果車輛ID不在計數列表中，將其添加進去
                if counter1.count(id) == 0:
                    counter1.append(id)

    # 繪製兩條檢測線和相應的文字
    cv2.line(frame, (274, cy1), (814, cy1), (255, 255, 255), 1)
    cv2.putText(frame, '1Line', (274, 318),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
    cv2.line(frame, (177, cy2), (927, cy2), (255, 255, 255), 1)
    cv2.putText(frame, '2Line', (181, 363),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
    
    # 繪製下行車輛和上行車輛的計數文字
    d = (len(counter))
    cv2.putText(frame, 'CarsDown:' + str(d), (60, 40),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
    u = (len(counter1))
    cv2.putText(frame, 'CarsUp:' + str(u), (60, 130),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
    
    # 顯示處理後的影格
    cv2.imshow("RGB", frame)
    
    # 如果按下 ESC 鍵，結束迴圈
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 釋放視訊捕捉物件和關閉所有視窗
cap.release()
cv2.destroyAllWindows()
