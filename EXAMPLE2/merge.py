import cv2,glob
import numpy as np

files = glob.glob('cropMOno\*.jpg') #要合併的圖形
n=len(files) #共有幾個檔案
spaceX = 10  #字元左邊空白寬度
spaceY = 8   #字元上面空白高度
offset=1     #每個字元間的間隔
img = cv2.imread(files[0])  #讀取要辨識的第一張圖形,取得高度、寬度
h,w=img.shape[0],img.shape[1]

#建立白色背景
bg = np.zeros((h+2*spaceY, (w+offset)*n+2*spaceX, 1), np.uint8)
bg.fill(255)  #設背景為白色

# 將車牌文字加入白色背景圖片中
for m,file in enumerate(files):
    gray = cv2.imread(file,0)  #讀取灰階圖形
    _,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  #轉為黑白
    for row in range(h):  #將文字圖片加入背景
        for col in range(w):
            bg[spaceY+row][spaceX+col+(w+offset)*m] = thresh[row][col] #擷取圖形   
cv2.imwrite('merge.jpg', bg) #存檔 
    
merge = cv2.imread("merge.jpg")  #讀取檔案
cv2.imshow("merge",merge) 
cv2.waitKey(0)  #按任意鍵結束
cv2.destroyAllWindows()