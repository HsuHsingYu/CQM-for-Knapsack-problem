
# Knapsack Problem Solver with D-Wave CQM Model

This project demonstrates how to solve the 0/1 Knapsack Problem using the **Constrained Quadratic Model (CQM)** provided by D-Wave's hybrid solver.

## Problem Description

The **Knapsack Problem** is a combinatorial optimization problem where you aim to select items with the maximum value without exceeding a weight capacity. In this example:

- **Objective**: Maximize the total value of selected items.
- **Constraint**: The total weight of selected items must not exceed the knapsack's capacity.

## How It Works

This implementation uses **D-Wave's CQM** framework to formulate and solve the problem.

### Features
- Uses the **Hybrid CQM Solver** for solving complex optimization problems.
- Handles large-scale problems with up to 100 items.
- Automatically selects the best solution based on the solver's output.

---

## Requirements

Ensure you have the following installed:

- Python 3.7 or later
- Required Python libraries:
  - `dimod`
  - `dwave-system`

You can install the dependencies using:
```bash
pip install dimod dwave-system
```

---

## Code Workflow

1. **Define the Problem**:
   - Items have a value and a weight.
   - The knapsack has a limited capacity.
2. **CQM Formulation**:
   - Define binary variables to represent item selection.
   - Maximize the total value of selected items as the objective.
   - Add a constraint to ensure the total weight does not exceed the capacity.
3. **Solve with Hybrid CQM Solver**:
   - Submit the CQM model to D-Wave's solver.
   - Extract and process the best solution.
4. **Output Results**:
   - Display selected items, total value, total weight, and computation time.

---

## Code Explanation

### 1. Define Items
Each item has a value and weight. Items are generated dynamically based on patterns:
```python
items = [Item(value=6 + (i // 10), weight=1 + (i // 10)) for i in range(num_items)]
```

### 2. Formulate the CQM Model
- **Objective Function**:
  Maximize the total value of selected items.
  ```python
  cqm.set_objective(-sum(items[i].value * x[i] for i in range(num_items)))
  ```
- **Weight Constraint**:
  Total weight of selected items must not exceed the knapsack capacity.
  ```python
  cqm.add_constraint(sum(items[i].weight * x[i] for i in range(num_items)) <= capacity, label='weight_constraint')
  ```

### 3. Solve the Model
Use D-Wave's **Hybrid CQM Solver** to find the optimal solution:
```python
sampler = LeapHybridCQMSampler()
solution = sampler.sample_cqm(cqm)
```

### 4. Extract Results
Process the solver's output to determine:
- Selected items
- Total value and weight
- Computation time

---

## Example Output

For a knapsack capacity of `275` and `100` items:

```plaintext
Selected item indices: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...]
Total value: 153
Total weight: 275
Total computation time: 3.7128 seconds
```

---

## How to Run

1. **Set Up API Key**:
   - Create an account on [D-Wave Leap](https://cloud.dwavesys.com/leap/).
   - Configure your API key locally using:
     ```bash
     dwave config create
     ```

2. **Run the Code**:
   Execute the Python script:
   ```bash
   python knapsack_cqm_solver.py
   ```

---

## Customization

### Modify Problem Parameters
You can adjust the following parameters in the code:
- **Knapsack Capacity**:
  ```python
  capacity = 275  # Change the total capacity
  ```
- **Number of Items**:
  ```python
  num_items = 100  # Change the total number of items
  ```
- **Item Value and Weight Patterns**:
  Modify the logic for generating item values and weights:
  ```python
  items = [Item(value=6 + (i // 10), weight=1 + (i // 10)) for i in range(num_items)]
  ```

---

## References

- [D-Wave Hybrid Solver Documentation](https://docs.dwavesys.com/docs/latest/)
- [Constrained Quadratic Model (CQM) Overview](https://docs.dwavesys.com/docs/latest/cqm_intro.html)

---
