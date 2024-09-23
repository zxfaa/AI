import cv2
import numpy as np

#建立桃紅色畫布
canvas = np.ones((200, 250, 3), dtype="uint8")
print(canvas.shape) #(200, 250, 3)
canvas[:] = (125, 40, 255) 
cv2.imshow('canvas', canvas)

bg = np.zeros((200, 250,1), np.uint8) #建立黑色背景畫布
print(bg.shape) #(200, 250, 1)
bg.fill(255)    #將黑色背景更改為白色背景

for j in range(200): #將圖片設為由 白->黑 漸層色
    for i in range(250):
      bg[j][i].fill(255-i)

cv2.imshow("bg", bg) 

cv2.waitKey(0)
cv2.destroyAllWindows()