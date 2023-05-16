import numpy as np
import heapq


def run_monte_carlo_simulation(tasks, num_iterations, distribution_type, num_participants):
    if distribution_type == 'normal':
        return monte_carlo_simulation_normal(tasks, num_iterations, num_participants)
    else:
        return monte_carlo_simulation_triangular(tasks, num_iterations, num_participants)


def monte_carlo_simulation_triangular(tasks, num_iterations, num_participants):
    task_times = np.random.triangular(
        [task['min'] for task in tasks],
        [task['likely'] for task in tasks],
        [task['max'] for task in tasks],
        size=(num_iterations, len(tasks))
    )
    return simulate_task_execution(task_times, num_participants)


def monte_carlo_simulation_normal(tasks, num_iterations, num_participants):
    task_times = np.random.normal(
        loc=[task['mean'] for task in tasks],
        scale=[task['std_dev'] for task in tasks],
        size=(num_iterations, len(tasks))
    )
    return simulate_task_execution(task_times, num_participants)


def simulate_task_execution(task_times, num_participants):
    total_time = np.zeros(task_times.shape[0])
    for i in range(task_times.shape[0]):
        heap = []
        for j in range(min(num_participants, len(task_times[i]))):
            heapq.heappush(heap, task_times[i][j])
        for j in range(num_participants, len(task_times[i])):
            min_time = heapq.heappop(heap)
            heapq.heappush(heap, min_time + task_times[i][j])
        total_time[i] = max(heap)
    return total_time
