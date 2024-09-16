import cv2;
import os;
os.chdir(os.path.dirname(__file__)) #設定目前目錄為工作目錄


cv2.namedWindow("ShowImage")
image1 = cv2.imread("media\\1.jpg")
image2 = cv2.imread("media\\2.jpg",0)

cv2.imshow("ShowImage1",image1)
cv2.imshow("ShowImage2",image2)
cv2.waitKey(0)
cv2.destroyAllWindows
