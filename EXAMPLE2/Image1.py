from PIL import Image
img = Image.open("media\\img01.jpg")
img.show()
w,h=img.size
print(w,h) #320 240
filename=img.filename
print(filename) #"media\img01.jpg