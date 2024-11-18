from ultralytics import YOLO
import numpy
import os

os.chdir(os.path.dirname(__file__)) #設定目前目錄為工作目錄

# load a pretrained YOLOv8n model
model = YOLO("yolov8n.pt", "v8")  

# predict on an image
detection_output = model.predict(source="inference/images/img0.JPG", conf=0.25, save=True) 

# Display tensor array
print(detection_output)

# Display numpy array
# 假設 detection_output[0] 是一個 tensor
print(detection_output[0].cpu().numpy())  # 先移到 CPU，再轉換為 numpy 陣列
