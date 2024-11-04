import tensorflow as tf
import os
from keras import layers, models 
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(__file__))  # 設定目前目錄為工作目錄

# 設定影像大小和批次大小
img_height, img_width = 180, 180
batch_size = 12

# 載入訓練集
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "C:/tranningData/train",
    image_size=(img_height, img_width),
    batch_size=batch_size
)

# 載入測試集
test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "C:/tranningData/test",
    image_size=(img_height, img_width),
    batch_size=batch_size
)

class_names = train_ds.class_names
print("Class names:", class_names)

# 顯示部分影像
plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
    for i in range(9):
        plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(class_names[labels[i]])
        plt.axis("off")
plt.show()

# 模型結構
model = models.Sequential([
    # 圖像預處理
    layers.Rescaling(1./255),
    
    # 卷積層 1
    layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.2),
    
    # 卷積層 2
    layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.3),
    
    # 分類層
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.4),  # 增加 Dropout
    layers.Dense(1, activation='sigmoid')
])

# 編譯模型
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 早停法
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

# 訓練模型
epochs = 30
history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=epochs,
    callbacks=[early_stopping]
)

# 評估測試準確度
test_loss, test_acc = model.evaluate(test_ds)
print(f'\nTest accuracy: {test_acc}')

# 繪圖
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(len(acc))

# 取得訓練和驗證的準確度、損失數值
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

# 列印數值
print("Epoch\tTraining Accuracy\tValidation Accuracy\tTraining Loss\tValidation Loss")
for i in range(len(acc)):
    print(f"{i+1}\t{acc[i]:.4f}\t\t{val_acc[i]:.4f}\t\t{loss[i]:.4f}\t\t{val_loss[i]:.4f}")

plt.figure(figsize=(12, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
