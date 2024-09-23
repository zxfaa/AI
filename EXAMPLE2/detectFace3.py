import cv2 
casc_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(casc_path)
image = cv2.imread("media\\person3.jpg")
faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags = cv2.CASCADE_SCALE_IMAGE)
imgheight=image.shape[0] #圖片高度
imgwidth=image.shape[1]  #圖片寬度
cv2.rectangle(image, (10,imgheight-20), (110,imgheight), (0,0,0), -1) #左下角黑色矩形
cv2.putText(image,"Find " + str(len(faces)) + " face!", (10,imgheight-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y),(x+w, y+h),(128,255,0),2)
cv2.namedWindow("facedetect")
cv2.imshow("facedetect", image)
cv2.waitKey(0)  
cv2.destroyWindow("facedetect")