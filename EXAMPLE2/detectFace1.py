import cv2  # 匯入 OpenCV 庫，用於圖像處理
import os   # 匯入 os 模組，用於處理目錄和檔案

# 設定當前腳本所在的目錄為工作目錄，以確保可以正確讀取相對路徑下的檔案
os.chdir(os.path.dirname(__file__))

# 指定人臉檢測的 Haar Cascade 模型的路徑
casc_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# 讀取 Haar Cascade 模型，建立一個人臉檢測的分類器
faceCascade = cv2.CascadeClassifier(casc_path)

# 讀取目標圖像 'person1.jpg'，這是我們要進行臉部檢測的圖像
image = cv2.imread("media\\person1.jpg")

# 使用人臉分類器來檢測圖像中的臉部
# scaleFactor：每次圖像縮放的比例，用來檢測不同大小的臉
# minNeighbors：每個候選矩形保留的最小鄰居數，數字越高，檢測越準確但可能漏檢
# minSize：可以檢測到的最小臉部大小
# flags：額外的標誌，用來調整圖像縮放和檢測算法
faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

# 取得圖像的高度和寬度，便於後續在圖像的指定位置繪製文字
imgheight = image.shape[0]  # 圖片高度
imgwidth = image.shape[1]   # 圖片寬度

# 在圖像的左下角繪製一個黑色矩形，用來顯示偵測到的臉部數量
cv2.rectangle(image, (10, imgheight - 20), (110, imgheight), (0, 0, 0), -1)

# 在黑色矩形上顯示檢測到的臉部數量，文字為白色
cv2.putText(image, "Find " + str(len(faces)) + " face!", (10, imgheight - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# 對每一個檢測到的臉部座標繪製一個矩形
# (x, y) 是矩形左上角座標，(w, h) 是矩形的寬度和高度
for (x, y, w, h) in faces:
    # 使用綠色 (BGR 顏色模式) 繪製臉部的矩形框，線條寬度為 2
    cv2.rectangle(image, (x, y), (x + w, y + h), (128, 255, 0), 2)

# 建立一個名為 'facedetect' 的視窗來顯示圖像
cv2.namedWindow("facedetect")

# 在視窗中顯示已標註臉部的圖像
cv2.imshow("facedetect", image)

# 等待用戶按下任意鍵後關閉視窗
cv2.waitKey(0)

# 關閉顯示圖像的視窗
cv2.destroyWindow("facedetect")
