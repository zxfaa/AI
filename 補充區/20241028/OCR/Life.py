import cv2

def showbitmap(row,col,bg,h,w):
    for y in range(row,row+h):
        print(str('{:0>2d}') .format(y)+":" ,end="")
        for x in range(col,col+w):
            print(bg[y][x],end=",")
        print()
    print() 
    
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

image = cv2.imread('7.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #灰階
_,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV) #轉為黑白
h=thresh.shape[0]
w=thresh.shape[1]
# print("h,w=",h,w) # 38,18

bg=thresh.copy()
showbitmap(0,0,bg,h,w)

lifearea=0 # 生命區塊
nn=0       # 每個生命區塊的生命數
life=[]    # 記錄每個生命區塊的生命數串列

for row in range(0,h):
   for col in range(0,w):
      if bg[row][col] == 255:
         nn = 1  #生命起源
         lifearea = lifearea + 1  #有生命區塊數
         area(row,col)  #以生命起源為起點探索每個生命區塊的總生命數
         life.append(nn)

print("lifearea=",lifearea) #生命區塊數
print(life)                 #該生命區塊的總生命數
maxlife=max(life)           #找到最大的生命數
indexmaxlife=life.index(maxlife) #找到最大的生命數的區塊編號
showbitmap(0,0,bg,h,w)  #顯示該文字的所有像素
 
for row in range(0,h):
   for col in range(0,w):
      if bg[row][col] == indexmaxlife+1:
          bg[row][col]=255
      else:
          bg[row][col]=0
showbitmap(0,0,bg,h,w)  
_,bg = cv2.threshold(bg, 127, 255, cv2.THRESH_BINARY_INV)  #轉為黑白        
cv2.imwrite('area.jpg', bg)  #存檔  

cv2.imshow('Frame', thresh)  #顯示圖形
cv2.moveWindow("Frame",500,450) # move 
cv2.imshow('bg', bg)  #顯示圖形
cv2.moveWindow("bg",500,550) # move 
key = cv2.waitKey(0)
cv2.destroyAllWindows()