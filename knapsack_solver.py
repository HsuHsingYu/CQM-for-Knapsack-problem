from dataclasses import dataclass
from dwave.system import LeapHybridCQMSampler
from dimod import ConstrainedQuadraticModel, Binary
import time  # 用於測量運行時間

# 定義物品類別
@dataclass
class Item:
    value: int
    weight: int

# 背包參數
capacity = 275
num_items = 100

# 根據規律生成物品資訊
items = [Item(value=6 + (i // 10), weight=1 + (i // 10)) for i in range(num_items)]

# 檢查生成的物品
for i, item in enumerate(items[:10]):  # 只打印前 10 個以檢查
    print(f"Item {i}: Value={item.value}, Weight={item.weight}")

# 定義 CQM 模型
cqm = ConstrainedQuadraticModel()

# 定義變量
x = [Binary(f'x_{i}') for i in range(num_items)]

# 目標函數：最大化價值
cqm.set_objective(-sum(items[i].value * x[i] for i in range(num_items)))

# 約束條件：總重量不得超過容量
cqm.add_constraint(sum(items[i].weight * x[i] for i in range(num_items)) <= capacity, label='weight_constraint')

# 測量運算時間
start_time = time.time()  # 記錄開始時間

# 使用混合解算器
sampler = LeapHybridCQMSampler()
solution = sampler.sample_cqm(cqm)

end_time = time.time()  # 記錄結束時間

# 獲取最佳解
best_solution = solution.first.sample
selected_items = [i for i in range(num_items) if best_solution[f'x_{i}'] == 1]

# 結果輸出
total_value = sum(items[i].value for i in selected_items)
total_weight = sum(items[i].weight for i in selected_items)
total_time = end_time - start_time  # 計算運行時間

print(f"選中的物品索引: {selected_items}")
print(f"總價值: {total_value}")
print(f"總重量: {total_weight}")
print(f"總計算時間: {total_time:.4f} 秒")  # 格式化輸出，保留 4 位小數