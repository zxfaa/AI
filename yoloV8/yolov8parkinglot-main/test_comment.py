# 導入 OpenCV 庫
import cv2
# 導入 Pandas 庫，用於數據處理
import pandas as pd
# 導入 NumPy 庫，用於數值計算
import numpy as np
# 從 Ultralytics 庫導入 YOLO 模型
from ultralytics import YOLO
# 導入 OS 库，用於處理文件和目錄
import os

# 設定當前目錄為腳本檔案所在目錄
os.chdir(os.path.dirname(__file__))

# 初始化 YOLO 模型，使用 'yolov8s.pt' 預訓練權重檔案
model = YOLO('yolov8s.pt')

# 定義滑鼠事件的回調函數


def RGB(event, x, y, flags, param):
    # 當滑鼠移動時觸發
    if event == cv2.EVENT_MOUSEMOVE:
        # 取得當前位置的 BGR 顏色值
        colorsBGR = [x, y]
        print(colorsBGR)


# 創建一個名為 'RGB' 的視窗並設定滑鼠回調函數
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# 讀取影片檔案
cap = cv2.VideoCapture('park.mp4')

# 讀取包含物件類別的檔案 'coco.txt'
my_file = open("coco_c.txt", "r")
data = my_file.read()
class_list = data.split("\n")
print(class_list)
count = 0

while True:
    # 讀取影片的一幀
    ret, frame = cap.read()
    count += 1
    # 每3幀處理一次
    if count % 3 != 0:
        continue

    # 調整影片大小為 (1020, 500)
    frame = cv2.resize(frame, (1020, 500))

    # 使用 YOLO 模型進行物件偵測
    results = model.predict(frame)
    # print(results)
    # 取得偵測結果的邊界框座標
    a = results[0].boxes.boxes
    px = pd.DataFrame(a).astype("float")
    # print(px)

    # 在影格上繪製邊界框和物件類別文字
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        # 在影格上繪製矩形框，(0, 255, 0) 為矩形框的顏色，2 為線寬度
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 在影格上繪製文字，str(d) 為文字內容，(x1, y1) 為文字位置
        # cv2.FONT_HERSHEY_COMPLEX 為字型，0.5 為字型大小，(255, 0, 0) 為文字顏色，1 為字型粗細
        # cv2.putText(frame, str(d), (x1, y1),
        #             cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
        # 在影格上繪製文字，顯示物件名稱而不是類別編號
        cv2.putText(frame, c, (x1, y1 - 10),  # 將文字位置稍微上移以避免重疊
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

    # 在 'RGB' 視窗中顯示當前影格
    cv2.imshow("RGB", frame)

    # 如果按下 ESC 鍵，則結束迴圈
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 釋放影片檔案和關閉所有視窗
cap.release()
cv2.destroyAllWindows()
