def emptydir(dirname):
    # 檢查資料夾是否存在，存在則刪除該資料夾及其內容
    if os.path.isdir(dirname):
        shutil.rmtree(dirname)  # 刪除資料夾及所有內容
        sleep(2)  # 稍微延遲，避免系統出錯
    os.mkdir(dirname)  # 建立一個新資料夾

from PIL import Image, ImageDraw  # 匯入Pillow中的Image和ImageDraw模組來進行圖片處理
import shutil, os  # 匯入shutil用來處理資料夾，os用來進行系統操作
from time import sleep  # 匯入sleep來延遲執行

os.chdir(os.path.dirname(__file__))

# 打開包含正樣本圖片資訊的檔案
fp = open('Haar-Training_carPlate/training/positive/info.txt', 'r')
lines = fp.readlines()  # 讀取檔案中的所有行，每一行是一個正樣本圖片的資訊
emptydir('picMark')  # 清空並重新建立 'picMark' 資料夾來存放標記後的圖片
print('開始繪製圖框！')

# 逐行處理檔案中的每一個正樣本資訊
for line in lines:
    data = line.split(' ')  # 將每行文字根據空格分割，轉換為資料列表
    img = Image.open('Haar-Training_carPlate/training/positive/' + data[0])  # 開啟指定路徑的圖片檔案
    draw = ImageDraw.Draw(img)  # 使用ImageDraw來進行繪圖操作
    n = data[1]  # 圖框數量（即該圖片中有多少個標記物件）

    # 依據圖框數量，逐一繪製圖框
    for i in range(int(n)):
        x = int(data[2+i*4])  # 圖框的左上角 x 座標
        y = int(data[3+i*4])  # 圖框的左上角 y 座標
        w = int(data[4+i*4])  # 圖框的寬度
        h = int(data[5+i*4])  # 圖框的高度
        draw.rectangle((x, y, x+w, y+h), outline='red')  # 使用紅色繪製矩形，表示標記的圖框

    filename = (data[0].split('/'))[-1]  # 從路徑中提取出圖片的檔案名稱
    img.save('picMark/' + filename)  # 將標記後的圖片存入 'picMark' 資料夾

fp.close()  # 關閉檔案
print('繪製圖框結束！')  # 繪製圖框結束的提示
