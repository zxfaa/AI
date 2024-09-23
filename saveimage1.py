import cv2
import os

os.chdir(os.path.dirname(__file__)) #設定目前目錄為工作目錄

cv2.namedWindow("ShowImage")

image= cv2.imread("media/1.jpg",0)
cv2.imshow("ShowImage",image)
cv2.imwrite("media/imageCopy1.jpg",image)
cv2.imwrite("media/imageCopy2.jpg",image,[int(cv2.IMWRITE_JPEG_QUALITY),50])
cv2.waitKey(0)
cv2.destroyAllWindows