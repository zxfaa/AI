import cv2
from PIL import Image
import numpy as np
gray = cv2.imread("media\\img01.jpg", 0) #以灰階模式開啟圖片
_,thresh = cv2.threshold(gray, 99, 255, cv2.THRESH_BINARY) #轉為黑白
cv2.imwrite("media\\thresh1.jpg", thresh) #存檔

img = Image.open('media\\img01.jpg')
w,h=img.size #320 240
img = img.convert('L')  #先轉換為灰階
for i in range(w):      #i為每一行
    for j in range(h):  #j為每一列
        if img.getpixel((i,j)) <99:  
            img.putpixel((i,j),(0))  #設為黑色
        else:
            img.putpixel((i,j),(255))#設為白色
img.save("media\\thresh2.jpg")       #存檔