import dimod
from dwave.system import LeapHybridCQMSampler
import time  # 用於計算執行時間

def read_knapsack_instance(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        n, c = map(int, lines[0].split())
        items = [tuple(map(int, line.split())) for line in lines[1:n+1]]
    return n, c, items

def solve_knapsack_cqm(n, capacity, items):
    cqm = dimod.ConstrainedQuadraticModel()

    # 定義變數
    x = {i: dimod.Binary(f'x_{i}') for i in range(n)}

    # 定義目標函數
    objective = dimod.quicksum(items[i][0] * x[i] for i in range(n))  # 最大化價值
    cqm.set_objective(-objective)

    # 添加約束條件
    weight_constraint = dimod.quicksum(items[i][1] * x[i] for i in range(n))
    cqm.add_constraint(weight_constraint <= capacity, label="Weight_Constraint")

    # 使用解算器
    start_time = time.time()  # 開始計時
    sampler = LeapHybridCQMSampler()
    solution = sampler.sample_cqm(cqm)
    end_time = time.time()  # 結束計時
    elapsed_time = end_time - start_time  # 計算執行時間

    # 找到最優解
    feasible_solutions = solution.filter(lambda d: d.is_feasible)
    if len(feasible_solutions) == 0:
        print("No feasible solution found!")
        return None, None, elapsed_time
    best_solution = feasible_solutions.first.sample
    best_energy = feasible_solutions.first.energy

    return best_solution, best_energy, elapsed_time

# 主程式
if __name__ == "__main__":
    file_path = "knapsack-01-instances-main/pisinger_instances_01_KP/large_scale/knapPI_1_10000_1000_1"  # 替換為您的檔案路徑
    n, capacity, items = read_knapsack_instance(file_path)

    # 解問題並計時
    best_solution, best_energy, elapsed_time = solve_knapsack_cqm(n, capacity, items)

    if best_solution:
        selected_items = [int(var.split('_')[1]) for var, val in best_solution.items() if val == 1]
        total_value = sum(items[i][0] for i in selected_items)
        total_weight = sum(items[i][1] for i in selected_items)

        print(f"\nTotal weight: {total_weight}/{capacity}")
        print(f"Total value: {total_value}")
        print(f"Solver energy: {best_energy}")

        if total_weight > capacity:
            print("Constraint violated: Total weight exceeds capacity.")
        else:
            print("Constraint satisfied: Solution is feasible.")

        print(f"\nTime taken to solve the problem: {elapsed_time:.2f} seconds.")