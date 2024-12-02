import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import *
import cvzone  # 用於物件追蹤的庫
# pip install cvzone
import os

os.chdir(os.path.dirname(__file__))  # 設定目前的目錄為工作目錄
model = YOLO('yolov8s.pt')  # 使用Yolov8s模型初始化YOLO物件

# 定義鼠標事件的回調函式


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)


# 創建一個名為'RGB'的視窗，並設置鼠標事件回調函式
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# 從影片文件'vidp.mp4'中讀取視頻
cap = cv2.VideoCapture('vidp.mp4')

# 讀取標籤文件'coco.txt'中的類別列表
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# 初始化計數、物件追蹤器、計數器列表等變數
count = 0
tracker = Tracker()
counter1 = []
counter2 = []
cy1 = 194
cy2 = 220
offset = 6

while True:
    # 讀取一幀的視頻
    ret, frame = cap.read()
    if not ret:
        break

    # 每三幀處理一次
    count += 1
    if count % 3 != 0:
        continue

    # 調整視頻幀大小為(1020, 500)
    frame = cv2.resize(frame, (1020, 500))

    # 使用YOLO模型預測畫面中的物體
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    # 提取類別為'person'的物體座標並放入列表
    list = []
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])

        c = class_list[d]
        if 'person' in c:
            list.append([x1, y1, x2, y2])

    # 使用物件追蹤器更新追蹤列表
    bbox_id = tracker.update(list)

    # 將每個追蹤到的物體在視頻幀中標記出來
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = int(x3 + x4) // 2
        cy = int(y3 + y4) // 2
        cv2.circle(frame, (cx, cy), 4, (255, 0, 255), -1)

    # 在畫面中標記兩條水平線
    cv2.line(frame, (3, 194), (1018, 194), (0, 255, 0), 2)
    cv2.line(frame, (5, 220), (1019, 220), (0, 255, 255), 2)

    # 顯示處理後的視頻幀
    cv2.imshow("RGB", frame)

    # 按下ESC鍵退出迴圈
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 釋放視頻捕捉器並關閉所有視窗
cap.release()
cv2.destroyAllWindows()
