from dataclasses import dataclass
from dwave.system import LeapHybridCQMSampler
from dimod import ConstrainedQuadraticModel, Binary
import time  # Used to measure runtime

# Define the item class
@dataclass
class Item:
    value: int
    weight: int

# Knapsack parameters
capacity = 275
num_items = 100

# Generate item information based on patterns
items = [Item(value=6 + (i // 10), weight=1 + (i // 10)) for i in range(num_items)]


# Define the CQM model
cqm = ConstrainedQuadraticModel()

# Define variables
x = [Binary(f'x_{i}') for i in range(num_items)]

# Objective function: Maximize value
cqm.set_objective(-sum(items[i].value * x[i] for i in range(num_items)))

# Constraint: Total weight must not exceed capacity
cqm.add_constraint(sum(items[i].weight * x[i] for i in range(num_items)) <= capacity, label='weight_constraint')

# Measure runtime
start_time = time.time()  # Record start time

# Use hybrid solver
sampler = LeapHybridCQMSampler()
solution = sampler.sample_cqm(cqm)

end_time = time.time()  # Record end time

# Get the best solution
best_solution = solution.first.sample
selected_items = [i for i in range(num_items) if best_solution[f'x_{i}'] == 1]

# Output results
total_value = sum(items[i].value for i in selected_items)
total_weight = sum(items[i].weight for i in selected_items)
total_time = end_time - start_time  # Calculate runtime

print(f"Selected item indices: {selected_items}")
print(f"Total value: {total_value}")
print(f"Total weight: {total_weight}")
print(f"Total computation time: {total_time:.4f} seconds")  # Format output with 4 decimal places