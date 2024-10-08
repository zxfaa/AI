import cv2

def show(image): # 顯示 (6,8)-(10,14) 點的儲存內容
    for y in range(8,14):     #總共有 6 列
        for x in range(6,10): #每一列有 4 個像素   
            print(image[y,x],end=" ")
        print()
    print()
    
img = cv2.imread('media\\face.jpg')  #讀取要辨識的圖形

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #灰階
print("gray.shape=",gray.shape) # (400, 400)
show(gray)

_,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)  #轉為黑白
print("thresh.shape=",thresh.shape) # (400, 400)
show(thresh)

gray2 = cv2.imread("media\\face.jpg", 0) #灰階模式
show(gray2)

_,thresh2 = cv2.threshold(gray2, 100, 200, cv2.THRESH_BINARY_INV) #轉為黑白
show(thresh2)