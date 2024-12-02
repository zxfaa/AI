import math  # 導入數學模組，用於計算距離


# 定義一個物件追蹤器的類別


class Tracker:
    def __init__(self):
        # 初始化一個空字典來存儲物體的中心點，格式：{物體ID: (cx, cy)}
        self.center_points = {}
        # 初始化ID計數器，用於給每個新物體分配唯一ID
        self.id_count = 0

    def update(self, objects_rect):
        # 創建一個空列表，用於存儲物體的邊界框和ID
        objects_bbs_ids = []

        # 遍歷所有檢測到的物體的邊界框
        for rect in objects_rect:
            # 解構方框的 (x, y) 位置和寬度 (w)、高度 (h)
            x, y, w, h = rect
            # 計算方框中心點的 x 座標和 y 座標
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # 假設目前檢測到的是新物體
            same_object_detected = False

            # 遍歷已存儲的物體中心點，檢查是否匹配
            for id, pt in self.center_points.items():
                # 計算當前物體與已知物體中心點之間的歐氏距離
                dist = math.hypot(cx - pt[0], cy - pt[1])

                # 如果距離小於閾值（例如 35 像素），則認為是同一物體
                if dist < 35:
                    # 更新該物體的中心點位置
                    self.center_points[id] = (cx, cy)
                    # 將物體的邊界框和ID添加到列表中
                    objects_bbs_ids.append([x, y, w, h, id])
                    # 標記為已檢測到相同物體
                    same_object_detected = True
                    break  # 匹配成功後，不需要檢查其他ID

            # 如果未找到匹配的物體，則將其視為新物體
            if not same_object_detected:
                # 分配新ID並存儲中心點
                self.center_points[self.id_count] = (cx, cy)
                # 將新物體的邊界框和ID添加到列表中
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                # 增加ID計數器，為下一個新物體準備
                self.id_count += 1


        # 創建一個新字典，用於保留仍在追蹤的物體
        new_center_points = {}
        # 遍歷所有檢測到的物體
        for obj_bb_id in objects_bbs_ids:
            # 解構邊界框信息，只取物體ID
            _, _, _, _, object_id = obj_bb_id
            # 從當前中心點字典中獲取該物體的中心點
            center = self.center_points[object_id]
            # 將中心點保留到新字典中
            new_center_points[object_id] = center

        # 更新物體中心點字典，刪除不再使用的ID
        self.center_points = new_center_points.copy()
        
        # 返回包含邊界框和ID的列表，供其他部分使用（例如繪圖）
        return objects_bbs_ids



""" 這個程式碼定義了一個簡單的物件追蹤器類別 (Tracker)，其中包含初始化方法 __init__ 和更新方法 update。以下是對每一行的詳細註解：

import math: 導入 Python 的數學模組，用於計算距離。

class Tracker:: 定義一個物件追蹤器的類別。

def __init__(self):: 初始化方法，用來初始化物件追蹤器的屬性。

self.center_points = {}: 用來存儲物體的中心位置的字典。

self.id_count = 0: 用來記錄物體ID的計數器，每次檢測到新的物體，計數器增加一。

def update(self, objects_rect):: 更新方法，用來更新物件追蹤器的狀態。

objects_bbs_ids = []: 用來存儲檢測到的物體的方框和ID的列表。

for rect in objects_rect:: 遍歷傳入的物體方框列表。

x, y, w, h = rect: 提取方框的位置和大小。

cx = (x + x + w) // 2: 計算方框的中心 x 座標。

cy = (y + y + h) // 2: 計算方框的中心 y 座標。

same_object_detected = False: 初始化標誌，表示是否檢測到相同的物體。

for id, pt in self.center_points.items():: 遍歷存儲的物體中心位置字典。

dist = math.hypot(cx - pt[0], cy - pt[1]): 計算新物體中心和已知物體中心的歐式距離。

if dist < 35:: 如果距離小於35，則視為檢測到相同的物體。

self.center_points[id] = (cx, cy): 更新已知物體的中心位置。

objects_bbs_ids.append([x, y, w, h, id]): 在列表中添加檢測到的物體的方框和ID。

same_object_detected = True: 更新標誌，表示檢測到相同的物體。

if same_object_detected is False:: 如果未檢測到相同的物體，執行以下操作。

self.center_points[self.id_count] = (cx, cy): 將新物體的中心位置添加到字典中。

objects_bbs_ids.append([x, y, w, h, self.id_count]): 在列表中添加檢測到的物體的方框和新的ID。

self.id_count += 1: 更新物體ID的計數器。

new_center_points = {}: 創建一個新的中心點字典。

for obj_bb_id in objects_bbs_ids:: 遍歷檢測到的物體的方框和ID的列表。

_, _, _, _, object_id = obj_bb_id: 提取物體的ID。

center = self.center_points[object_id]: 從原中心點字典中獲取中心位置。

new_center_points[object_id] = center: 在新的中心點字典中添加中心位置。

self.center_points = new_center_points.copy(): 更新中心點字典，刪除不再使用的ID。

return objects_bbs_ids: 返回檢測到的物體的方框和ID的列表。






 """
