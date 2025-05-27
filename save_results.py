import csv
import os
import pprint

RESULTS_FOLDER = 'results'

# Filenames
STARTUP_TIMES_FILENAME = 'startup_time.csv'
CPU_USAGE_FILENAME = 'cpu_usage.csv'
MEMORY_USAGE_FILENAME = 'memory_usage.csv'

# Fieldnames
STARTUP_TIMES_FIELDNAME = 'Startup Time (ms)'
CPU_USAGE_FIELDNAME = 'CPU Usage (kC)'
MEMORY_USAGE_FIELDNAME = 'Memory Usage (kB)'

def save_general_results(version: str, measurements: dict, cpu_metric: str, memory_metric: str):
    path = __create_path(version)

    cpu_usage = __get_by_metric(cpu_metric, measurements)
    __save_cpu_usage(path, cpu_usage)

    memory_usage = __get_by_metric(memory_metric, measurements)
    __save_memory_usage(path, memory_usage)

def save_startup_results(version: str, measurements: list[float]):
    path = __create_path(version)
    __save_startup_time(path, measurements)

def __get_by_metric(metric: str, measurements: dict) -> list:
    values = map(lambda x: (x[0], x[1].get(metric)), list(measurements.items()))
    return list(filter(lambda x: x[1] != None, values))

def __save_startup_time(path: str, measurements: list[float]):
    in_ms = list(map(lambda x: x * 1000, measurements))
    with open(f'{path}/{STARTUP_TIMES_FILENAME}', 'w') as file:
        fieldnames = [STARTUP_TIMES_FIELDNAME]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        for measurement in in_ms:
            writer.writerow([measurement])

def __save_cpu_usage(path: str, cpu_usage: list[tuple]):
    __save_generic_usage(path, CPU_USAGE_FILENAME, cpu_usage)

def __save_memory_usage(path: str, memory_usage: list[tuple]):
    __save_generic_usage(path, MEMORY_USAGE_FILENAME, memory_usage)

def __save_generic_usage(path: str, filename: str, measurements: list[tuple]):
    with open(f'{path}/{filename}', 'w') as file:
        fieldnames = list(map(lambda x: x[0], measurements))
        values = list(map(lambda x: x[1], measurements))
        value_count = min(map(lambda x: len(x), values))
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        for i in range(value_count):
            row = list(map(lambda x: x[i], values))
            writer.writerow(row)

def __create_path(version: str) -> str:
    path = f'{RESULTS_FOLDER}/{version}'
    if not os.path.exists(path): os.makedirs(path)
    return path
