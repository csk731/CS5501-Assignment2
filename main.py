import random, time
import matplotlib.pyplot as plt

def linear_search(lst, key):
    count = 0
    for i in range(0, len(lst)):
        count += 2
        if lst[i] == key:
            return True, count
    return False, count + 1

def sentinel_search(lst, key):
    count = 0
    n = len(lst)
    lst.append(key)
    i = 0
    while lst[i] != key:
        count += 1
        i += 1
    lst.pop()
    return (i < n), count + 1
    
def binary_search(lst, key):
    count = 0
    low = 0
    high = len(lst) - 1
    while low <= high:
        count += 1
        
        mid = (low + high) // 2
        count += 1
        if lst[mid] == key:
            return True, count
        elif key < lst[mid]:
            high = mid - 1
        else:
            low = mid + 1
        count += 1
    return False, count + 1
    
def ternary_search(lst, key):
    count = 0
    low = 0
    high = len(lst) - 1
    while low <= high:
        count += 1
        
        third = (high - low) // 3
        mid1 = low + third
        mid2 = high - third
        count += 1
        if lst[mid1] == key:
            return True, count
        count += 1
        if lst[mid2] == key:
            return True, count
            
        count += 2
        if key < lst[mid1]:
            high = mid1 - 1
        elif key > lst[mid2]:
            low = mid2 + 1
        else:
            low = mid1 + 1
            high = mid2 - 1
    return False, count + 1


'''
Experiment
'''
sizes = [1000, 5000, 10000, 50000, 100000]

algorithms = {
    "Linear Search": linear_search,
    "Sentinel Search": sentinel_search,
    "Binary Search": binary_search,
    "Ternary Search": ternary_search
}

# 5 Arbitary keys I have chosen for the sake of average case.
cases = {
    "beginning": "First Element",
    "middle": "Middle Element",
    "end": "Last Element",
    "absent": "Key Absent",
    "random": "Random Key"
}

results = {alg: {case: {"n": [], "comparisons": [], "time": []} for case in cases} for alg in algorithms}

for alg_name, func in algorithms.items():
    # print(f"Running experiment for {alg_name}")
    for n in sizes:
        # print(f"  List size: {n}")
        lst = [random.randint(0, 1000) for _ in range(n)]
        if alg_name in ["Binary Search", "Ternary Search"]:
            lst.sort()

        for case_key in cases:
            if case_key == "beginning":
                key = lst[0]
            elif case_key == "middle":
                key = lst[len(lst) // 2]
            elif case_key == "end":
                key = lst[-1]
            elif case_key == "absent":
                key = random.randint(1001, 2000)
            elif case_key == "random":
                key = random.choice(lst) if random.random() > 0.5 else random.randint(0, 1001)

            start_time = time.perf_counter()
            found, comparisons = func(lst, key)
            end_time = time.perf_counter()

            results[alg_name][case_key]["n"].append(n)
            results[alg_name][case_key]["comparisons"].append(comparisons)
            results[alg_name][case_key]["time"].append((end_time - start_time) * 1000)  # Convert to ms

# Tables
for alg_name in algorithms:
    print(f"\nResults for {alg_name}:")
    
    # Comparisions
    print("-" * 80)
    print("{:<10} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format(
        "List Size", "Beg Comp", "Mid Comp", "End Comp", "Absent Comp", "Rand Comp", "Avg Comp"
    ))
    print("-" * 80)
    
    for i, n in enumerate(sizes):
        comp_values = [results[alg_name][case_key]["comparisons"][i] for case_key in cases]
        avg_comparisons = sum(comp_values) / len(comp_values)
        print("{:<10} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12.2f}".format(
            n, *comp_values, avg_comparisons
        ))
    
    # Run Time
    print("\n" + "-" * 80)
    print("{:<10} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format(
        "List Size", "Beg Time", "Mid Time", "End Time", "Absent Time", "Rand Time", "Avg Time (ms)"
    ))
    print("-" * 80)
    
    for i, n in enumerate(sizes):
        time_values = [results[alg_name][case_key]["time"][i] for case_key in cases]
        avg_time = sum(time_values) / len(time_values)
        print("{:<10} {:<12.6f} {:<12.6f} {:<12.6f} {:<12.6f} {:<12.6f} {:<12.6f}".format(
            n, *time_values, avg_time
        ))


# Plots
# Graph 1: Average Comparisons for all algorithms
plt.figure(figsize=(10, 6))
for alg_name in algorithms:
    avg_comparisons_list = []
    for i in range(len(sizes)):
        avg_comp = sum(results[alg_name][case]["comparisons"][i] for case in cases) / len(cases)
        avg_comparisons_list.append(avg_comp)
    plt.plot(sizes, avg_comparisons_list, marker='o', label=alg_name)

plt.xlabel("List Size (n)")
plt.ylabel("Average Comparisons (log scale)")
plt.title("Average Comparisons vs List Size for All Algorithms")
plt.legend()
plt.grid(True)
plt.yscale('log')
plt.tight_layout()
plt.show()

# Graph 2: Average Time for all algorithms
plt.figure(figsize=(10, 6))
for alg_name in algorithms:
    avg_time_list = []
    for i in range(len(sizes)):
        avg_t = sum(results[alg_name][case]["time"][i] for case in cases) / len(cases)
        avg_time_list.append(avg_t)
    plt.plot(sizes, avg_time_list, marker='o', label=alg_name)

plt.xlabel("List Size (n)")
plt.ylabel("Average Time (ms)")
plt.title("Average Time vs List Size for All Algorithms")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()