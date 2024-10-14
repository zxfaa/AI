from PIL import Image
import os
os.chdir(os.path.dirname(__file__))
img = Image.open("media\\img01.jpg")
imggray = img.convert('L') #轉換為灰階

imggray.save("media\\gray01.jpg")