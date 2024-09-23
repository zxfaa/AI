from PIL import Image,ImageDraw
from PIL import ImageFont

img = Image.new("RGB",(300,400),"lightgray") #淡灰色
drawimg=ImageDraw.Draw(img)

#繪圓
drawimg.ellipse((50,50,250,250),width=3,outline="gold")# 臉
#繪多邊形
drawimg.polygon([(100,90),(120,130),(80,130)],fill="brown",outline="red") #左眼精
drawimg.polygon([(200,90),(220,130),(180,130)],fill="brown",outline="red")#右眼精
#繪矩形
drawimg.rectangle((140,140,160,180),fill="blue",outline="black") #鼻子
#繪橢圓
drawimg.ellipse((100,200,200,220),fill="red") #嘴巴   
#繪文字
drawimg.text((130,280),"e-happy",fill="orange")             #文字一
myfont=ImageFont.truetype("C:\Windows\Fonts\mingliu.ttc",16)
drawimg.text((110,320),"文淵閣工作室",fill="red",font=myfont) #文字二 
img.show()
img.save("media\\happyface.png")