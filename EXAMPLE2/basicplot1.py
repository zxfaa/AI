import cv2, numpy,os

os.chdir(os.path.dirname(__file__))  # 設定目前的目錄為工作目錄
cv2.namedWindow("plot")
image = cv2.imread("media\\background.jpg")
cv2.line(image, (50,50), (500,200), (255,0,0), 2)        #藍色直線
cv2.rectangle(image, (100,200), (180,300), (0,255,0), 3) #綠色空心矩形
cv2.rectangle(image, (300,200), (350,260), (0,0,255), -1)#紅色實心矩形
cv2.circle(image, (500,300), 40, (255,255,0), -1)        #實心圓
pts = numpy.array([[300,300],[300,340],[350,320]], numpy.int32)
# cv2.polylines(image, [pts], True, (0,255,255), 2)        #黃色多邊形
cv2.polylines(image, [pts], True, (0,255,255), 2)        #黃色多邊形
cv2.putText(image,"background.jpg", (20,420), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)#文字
cv2.imshow("plot", image) 
cv2.waitKey(0)
cv2.destroyAllWindows()