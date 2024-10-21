import os
os.chdir(os.path.dirname(__file__))  # 設定工作目錄為當前檔案所在的目錄

# 讀取 info.txt 檔案，這個檔案包含正樣本圖片的路徑及圖框標註資料
fp = open('Haar-Training_carPlate/training/positive/info.txt', 'r')
lines = fp.readlines()  # 讀取所有行的資料
rettext = ''  # 用來存放轉換後的結果
print('開始轉換圖框！')

# 逐行處理 info.txt 中的每一個正樣本圖片資訊
for line in lines:
    data = line.split(' ')  # 將每行根據空格切割成資料列表
    n = data[1]  # 圖框數量
    rettext += data[0] + ' ' + n + ' '  # 將圖片路徑與圖框數量寫入新資料

    # 處理每一個標註的圖框
    for i in range(int(n)):
        x = float(data[2 + i * 4])  # 左上角 x 座標
        y = float(data[3 + i * 4])  # 左上角 y 座標
        w = float(data[4 + i * 4])  # 圖框寬度
        h = float(data[5 + i * 4])  # 圖框高度

        # 檢查寬高比是否小於 3.8
        if (w / h) < 3.8:
            newW = h * 3.8  # 如果寬高比太小，則設定新的寬度
            x -= int((newW - w) / 2)  # 調整 x 座標，確保框保持居中
            if x <= 0:  # 防止 x 超出圖片邊界
                x = 0
            w = int(newW)  # 更新寬度為新的寬度

        # 將調整後的 x, y, w, h 資料存回 rettext
        rettext += str(int(x)) + ' ' + data[3 + i * 4] + ' ' + str(int(w)) + ' ' + data[5 + i * 4]

fp.close()  # 關閉檔案

# 將轉換後的結果寫回到 info.txt 檔案
fp = open('Haar-Training_carPlate/training/positive/info.txt', 'w')
fp.write(rettext)  # 寫入新的資料
fp.close()
print('轉換圖框結束！')
