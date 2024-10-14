from PIL import Image
import glob

path = 'Haar-Training_carPlate/training/positive/'
fp = open(path + 'info.txt', 'r')
lines = fp.readlines()  #讀取所有文字
count =  len(glob.glob("carPlate/*.bmp")) #圖片數，產生的圖片編號由此繼續
if len(lines)>count:
    print("新圖片已產生過!")
else:    
    rettext = ''
    print('開始產生新圖片！')    
    for line in lines:
        data = line.split(' ')
        img = Image.open(path + data[0])  #讀入圖形檔
        x = int(data[2])  #圖形X坐標
        y = int(data[3])  #圖形Y坐標
        w = int(data[4])  ##圖形寬
        h = int(data[5])  ##圖形高
        reduceW = 30  #減少的的寬度
        reduceH = int(reduceW*0.75)  #減少的的高度
        multi = float(300/(300-reduceW))  #原圖與新圖比例
        neww = int(w*multi)  #新圖的寬
        newh = int(h*multi)  #新圖的高
        #移除左上角圖
        if (x-reduceW)>5 and (y-reduceH)>5:  #左上角有空間才移除左上角
            count += 1  #編號加1,此數值會做為檔名用
            newimg = img.crop((reduceW, reduceH, 300, 225))  #擷取圖形
            newimg = newimg.resize((300, 225), Image.ANTIALIAS)  #放大圖形
            newimg.save(path + 'rawdata/bmpraw{:0>3d}.bmp'.format(count), 'bmp')  #存檔
            newx = int((x-reduceW)*multi-reduceW*(multi-1)/2)  #新圖X坐標
            newy = int((y-reduceH)*multi-reduceH*(multi-1)/2)  #新圖Y坐標            
            rettext = rettext+'rawdata/bmpraw{:0>3d}.bmp'.format(count)+' '+'1'+' '+str(newx)+' '+str(newy)+' '+str(neww)+' '+str(newh)+'\n'  #記錄新圖資料
        #移除右上角圖
        if (x+w)<(300-reduceW-5) and y>(reduceW+5):
            count += 1
            newimg = img.crop((0, reduceH, (300-reduceW), 225))
            newimg = newimg.resize((300, 225), Image.ANTIALIAS)
            newimg.save(path + 'rawdata/bmpraw{:0>3d}.bmp'.format(count), 'bmp')
            newx = int(x*multi)
            newy = int((y-reduceH)*multi)
            rettext = rettext+'rawdata/bmpraw{:0>3d}.bmp'.format(count)+' '+'1'+' '+str(newx)+' '+str(newy)+' '+str(neww)+' '+str(newh)+'\n'
        #移除左下角圖
        if (x-reduceW)>5 and (y+h)<(225-reduceH-5):
            count += 1
            newimg = img.crop((reduceW, 0, 300, 225-reduceH))
            newimg = newimg.resize((300, 225), Image.ANTIALIAS)
            newimg.save(path + 'rawdata/bmpraw{:0>3d}.bmp'.format(count), 'bmp')
            newx = int((x-reduceW)*multi)
            newy = int(y*multi)
            rettext = rettext+'rawdata/bmpraw{:0>3d}.bmp'.format(count)+' '+'1'+' '+str(newx)+' '+str(newy)+' '+str(neww)+' '+str(newh)+'\n'
        #移除右下角圖
        if (x+w)<(300-reduceW-5) and (y+h)<(225-reduceH-5):
            count += 1
            newimg = img.crop((0, 0, (300-reduceW), 225-reduceH))
            newimg = newimg.resize((300, 225), Image.ANTIALIAS)
            newimg.save(path + 'rawdata/bmpraw{:0>3d}.bmp'.format(count), 'bmp')
            newx = int(x*multi)
            newy = int(y*multi)
            rettext = rettext+'rawdata/bmpraw{:0>3d}.bmp'.format(count)+' '+'1'+' '+str(newx)+' '+str(newy)+' '+str(neww)+' '+str(newh)+'\n'

    fp.close()
    
    fpmake = open(path + 'Info.txt', 'a')  #以新增資料方式開啟檔案
    fpmake.write(rettext)  #寫入檔案
    fpmake.close()
    print('產生新圖片結束！')