import cv2
img = cv2.imread('media\\person1.jpg') #讀取要辨識的圖形
print("img.shape=",img.shape) # (533, 800, 3)        
cv2.imshow("win1", img) 

x,y,w,h=341,76,125,125
face = img[y: y + h, x: x + w]    #取得臉部圖形

x,y,w,h=341,76,125,125
for row in range(y,y+y):     #總共有 h 列(125列)
    for col in range(x,x+w): #每一列有 w 個像素 (125個像素)  
        print(img[row,col],end=" ")
    print()
print()

for row in range(y,y+h):     #總共有 h 列(125列)
    for col in range(x,x+w): #每一列有 w 個像素 (125個像素) 
        # 改變人臉的 B、G 值，R 值不變
        img[row,col][0]=0    #設定 B 值為 0
        img[row,col][1]=50   #設定 G 值為 50

cv2.imshow("win2", img) 
cv2.waitKey(0)  #按任意鍵結束
cv2.destroyAllWindows()