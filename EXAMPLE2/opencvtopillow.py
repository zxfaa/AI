import cv2
from PIL import Image 
img = cv2.imread('media\\img01.jpg') #OpenCV預設格式是 BGR
cv2.imshow("OpenCV",img)

# OpenCV 轉 Pillow
image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
image.show()
cv2.waitKey(0)
cv2.destroyAllWindows()