import math


class Tracker:
    def __init__(self):
        # 存儲對象的中心位置
        self.center_points = {}
        # 保持id的計數
        # 每次檢測到新的對象 id 時，計數將增加 1
        self.id_count = 0

    def update(self, objects_rect):
        # 對象框和 ID
        objects_bbs_ids = []

        # 獲取新對象的中心點
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # 查明是否已經檢測到該對象
            same_object_detected = False
            # 在這一步我們通過新物體相當於之前標記過各個物體的位置，判斷新檢測到的一個物體是否為以前標記的物體。
            # 循環變量id為物體標記,pt為各個物體中心點坐標（pt[0] = x, pt[1] = y）
            for id, pt in self.center_points.items():
                # math.hypot(x, y)計算該點到原點的距離，相當於math.sqrt(x * x + y * y)。
                # 這一函數用於算出當前物體和已記錄的第id個物體之間距離絕對值。
                # 如果此值小於25，我們認為這兩個物體為同一個。接下來更新第id物體中心點坐標，並把更新後坐標和id添加到objects_bbs_ids，
                # 該二維列表保存每個物體的x,y坐標及長寬
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 35:
                    self.center_points[id] = (cx, cy)
#                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # 如果沒有任何一個已標記的物體和被檢測物體坐標相近，及判斷該物體為新物體。
            # 把新物體賦予新id(id_count += 1)，並添加到center_points和objects_bbs_ids里
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # 用於刪除已消失的目標，防止center_points里保存太多無用坐標。
        # 我們將id存在在objects_bbs_ids里面的物體在center_points里予以保留，對剩余的物體隨著更新刪除。
        # objects_bbs_ids里面為存在在本次函數調用時這一幀的所有已有和新添加的物體。
        self.center_points = new_center_points.copy()
        return objects_bbs_ids
