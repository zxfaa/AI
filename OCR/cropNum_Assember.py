def area(row, col):
    global nn
    if bg[row][col] != 255:
        return
    bg[row][col] = lifearea #記錄生命區的編號
    if col>1: #左方
        if bg[row][col-1]==255:
            nn +=1
            area(row,col-1)
    if col< w-1: #右方
        if bg[row][col+1]==255:
            nn +=1
            area(row,col+1)             
    if row>1: #上方
        if bg[row-1][col]==255:
            nn+=1            
            area(row-1,col)
    if row<h-1: #下方
        if bg[row+1][col]==255:
            nn+=1            
            area(row+1,col)            

import cv2,os
import numpy as np

os.chdir(os.path.dirname(__file__))
image = cv2.imread('7238N2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #灰階
_,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV) #轉為黑白
contours1 = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #尋找輪廓
contours = contours1[0]   #取得輪廓

letter_image_regions = [] #文字圖形串列
for contour in contours:  #依序處理輪廓
    (x, y, w, h) = cv2.boundingRect(contour)  #單一輪廓資料
    letter_image_regions.append((x, y, w, h)) #輪廓資料加入串列
letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])  #按X坐標排序

#先計算可以擷取的字元數
count=0  #計算共擷取多少個字元
for box in letter_image_regions:  #依序處理輪廓資料
    x, y, w, h = box        
    # x 必須介於 2~125 且寬度在 5~26、高度在 20~39 才是文字
    if x>=2 and x<=125 and w>=5 and w<=26 and h>=20 and h<40:
        count +=1   
        
if count<6: #若字元數不足，可能是有兩個字元連在一起，將字元寬度放寬再重新擷取
    wmax=35
else:
    wmax=26 #正常字元寬度
    
nChar=0 #計算共擷取多少個字元
letterlist = [] #儲存擷取的字元坐標 
for box in letter_image_regions:  #依序處理輪廓資料
    x, y, w, h = box        
    # x 必須介於 2~125 且寬度在 5~wmax、高度在 20~39 才是文字
    if x>=2 and x<=125 and w>=5 and w<=wmax and h>=20 and h<40:
        nChar +=1 
        letterlist.append((x, y, w, h)) #儲存擷取的字元

#去除雜點    
for i in range(len(thresh)):  #i為高度
    for j in range(len(thresh[i])): #j為寬度  
        if thresh[i][j] == 255:     #顏色為白色
            count = 0 
            for k in range(-2, 3):
                for l in range(-2, 3):
                    try:
                        if thresh[i + k][j + l] == 255: #若是白點就將count加1
                            count += 1
                    except IndexError:
                        pass
            if count <= 6:  #週圍少於等於6個白點
                thresh[i][j] = 0  #將白點去除 
                
real_shape=[]
for i,box in enumerate(letterlist):  #依序擷取所有的字元
    x, y, w, h = box        
    bg=thresh[y:y+h, x:x+w]
    
    # 去除崎鄰地 
    if i==0 or i==nChar: # 只去除第一字元和最後字元的崎鄰地
        lifearea=0 # 生命區塊
        nn=0       # 每個生命區塊的生命數
        life=[]    # 記錄每個生命區塊的生命數串列            
        for row in range(0,h):
            for col in range(0,w):
              if bg[row][col] == 255:
                  nn = 1  #生命起源
                  lifearea = lifearea + 1  #生命區塊數
                  area(row,col)  #以生命起源為起點探索每個生命區塊的總生命數
                  life.append(nn)

        maxlife=max(life) #找到最大的生命數
        indexmaxlife=life.index(maxlife) #找到最大的生命數的區塊編號          
              
        for row in range(0,h):
            for col in range(0,w):
              if bg[row][col] == indexmaxlife+1:
                  bg[row][col]=255
              else:
                  bg[row][col]=0  
                  
    real_shape.append(bg) #加入字元               

#在圖片週圍加白色空白OCR才能辨識
newH, newW = thresh.shape

space = 8  #空白寬度
offset=2
bg = np.zeros((newH+space*2, newW+space*2+nChar*3, 1), np.uint8)  #建立背景
bg.fill(0)  #背景黑色

# 將車牌文字加入黑色背景圖片中
for i,letter in enumerate(real_shape):
    h=letter.shape[0]   #原來文字圖形的高、寬
    w=letter.shape[1]
    x=letterlist[i][0]  #原來文字圖形的位置
    y=letterlist[i][1]
    for row in range(h):#將文字圖片加入背景
        for col in range(w):
            bg[space+y+row][space+x+col+i*offset] = letter[row][col] #擷取圖形
           
_,bg = cv2.threshold(bg, 127, 255, cv2.THRESH_BINARY_INV) #轉為白色背景、黑色文字                 
cv2.imwrite('assember.jpg', bg) #存檔          

cv2.imshow('image', image)     #顯示原始圖形
cv2.imshow('bg', bg)           #顯示組合的字元
cv2.moveWindow("image",500,250)#將視窗移到指定位置
cv2.moveWindow("bg",500,350)   #將視窗移到指定位置     
key = cv2.waitKey(0)           #按任意鍵結束
cv2.destroyAllWindows() 