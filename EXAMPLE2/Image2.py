from PIL import Image
img = Image.open("media\\img01.jpg")
w,h=img.size #320 240

img1=img.resize((w*2,h))
img1.save("media\\resize01.jpg")