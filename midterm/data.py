import os
import shutil
import random

# 原始資料夾
base_dir = 'C:/tranningData'  # 根資料夾
cats_dir = 'C:/tranningData/cats'  # 貓圖片資料夾
dogs_dir = 'C:/tranningData/dogs'  # 狗圖片資料夾

# 獲取貓和狗圖片的檔名
cat_files = [f for f in os.listdir(cats_dir) if f.endswith(('.jpg', '.png'))]
dog_files = [f for f in os.listdir(dogs_dir) if f.endswith(('.jpg', '.png'))]

print(f'Cats: {len(cat_files)}')
print(f'Dogs: {len(dog_files)}')

# 清空資料夾的函數
def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

# 目標資料夾
train_cats_dir = os.path.join(base_dir, 'train', 'cats')
train_dogs_dir = os.path.join(base_dir, 'train', 'dogs')
test_cats_dir = os.path.join(base_dir, 'test', 'cats')
test_dogs_dir = os.path.join(base_dir, 'test', 'dogs')

# 創建目標資料夾
os.makedirs(train_cats_dir, exist_ok=True)
os.makedirs(train_dogs_dir, exist_ok=True)
os.makedirs(test_cats_dir, exist_ok=True)
os.makedirs(test_dogs_dir, exist_ok=True)

# 讀取所有貓和狗的圖片路徑
cat_files = [os.path.join(cats_dir, f) for f in os.listdir(cats_dir) if f.endswith(('.jpg', '.png'))]
dog_files = [os.path.join(dogs_dir, f) for f in os.listdir(dogs_dir) if f.endswith(('.jpg', '.png'))]

# 隨機打亂數據
random.shuffle(cat_files)
random.shuffle(dog_files)

# 計算分配的數量
num_train_cats = int(0.8 * len(cat_files))
num_train_dogs = int(0.8 * len(dog_files))

# 將圖片分配到訓練和測試資料夾
for cat_file in cat_files[:num_train_cats]:
    shutil.copy(cat_file, train_cats_dir)

for cat_file in cat_files[num_train_cats:]:
    shutil.copy(cat_file, test_cats_dir)

for dog_file in dog_files[:num_train_dogs]:
    shutil.copy(dog_file, train_dogs_dir)

for dog_file in dog_files[num_train_dogs:]:
    shutil.copy(dog_file, test_dogs_dir)

# 檢查分配後的資料夾圖片數量
print(f'Training Cats: {len(os.listdir(train_cats_dir))}')
print(f'Training Dogs: {len(os.listdir(train_dogs_dir))}')
print(f'Testing Cats: {len(os.listdir(test_cats_dir))}')
print(f'Testing Dogs: {len(os.listdir(test_dogs_dir))}')

print("數據分配完成！")
