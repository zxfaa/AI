from PIL import Image
img = Image.open("media\\img01.jpg")
imggray = img.convert('L') #轉換為灰階

imggray.save("media\\gray01.jpg")