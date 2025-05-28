import json
import os
import pprint
import time
from save_results import *

# Command Building
__START_TEST_COMMAND = 'xcodebuild test'
__SCHEME_ARG = '-scheme MyTerminal'
__PROJECT_ARG = '-project'
__DESTINATION_ARG = '-destination'
__GENERAL_TESTING_ARG = '-only-testing:MyTerminalUITests/MyTerminalUITests'
__STARTUP_TESTING_ARG = '-only-testing:MyTerminalUITests/MyTerminalStartupTests'

# Relevant metrics
CPU_CYCLES_KC = 'CPU Cycles'
ABSOLUTE_MEMORY_KB = 'Absolute Memory Physical'
STARTUP_TIME_S = 'Duration'

# Other
__VALUES_KEY = 'values: '
__VERSION = 'KMP'
__STARTUP_ITERATIONS = 10

def main():
    project_path = '/Users/mitchell.tol/Projects/MyTerminal/KMP/myterminal-kmp-ios'
    device_id = '00008101-001D04260190001E'

    # CPU and Memory
    start_time = time.time()
    general_stream = __run_test(project_path, device_id)
    end_time = time.time()
    metrics_lines = general_stream.splitlines()
    grouped = __group_results(metrics_lines, [LOAD_FLIGHTS, OPEN_DETAILS, BOOKMARK_FLIGHT, LOAD_BOOKMARS])
    parsed = __parse_results(grouped)
    pprint.pp(parsed)
    save_general_results(__VERSION, parsed, CPU_CYCLES_KC, ABSOLUTE_MEMORY_KB)
    print(f'Total time taken for general benchmark: {end_time - start_time}s')

    # Startup
    startup_results = []
    start_time = time.time()
    for _ in range(__STARTUP_ITERATIONS):
        startup_stream = __run_startup_test(project_path, device_id)
        metrics_lines = startup_stream.splitlines()
        grouped = __group_results(metrics_lines, [STARTUP])
        parsed = __parse_startup_results(grouped)
        if parsed != None: startup_results.append(parsed)
    end_time = time.time()
    print(startup_results)
    save_startup_results(__VERSION, startup_results)
    print(f'Total time taken for startup time benchmark: {end_time - start_time}s')

def __run_test(project_path: str, device_id: str) -> str:
    destination = f'\'id={device_id}\''
    return os.popen(f'{__START_TEST_COMMAND} {__SCHEME_ARG} {__PROJECT_ARG} {project_path}/MyTerminal.xcodeproj ' + 
             f'{__DESTINATION_ARG} {destination} {__GENERAL_TESTING_ARG} | grep "{project_path}" | grep "Test Case" ' + 
             f'| grep -e "{CPU_CYCLES_KC}" -e "{ABSOLUTE_MEMORY_KB}"').read()

def __run_startup_test(project_path: str, device_id: str) -> str:
    destination = f'\'id={device_id}\''
    return os.popen(f'{__START_TEST_COMMAND} {__SCHEME_ARG} {__PROJECT_ARG} {project_path}/MyTerminal.xcodeproj ' + 
             f'{__DESTINATION_ARG} {destination} {__STARTUP_TESTING_ARG} | grep "{project_path}" | grep "Test Case" ' + 
             f'| grep -e "{STARTUP_TIME_S}"').read()

def __group_results(lines: list[str], test_names: list[str]) -> dict:
    result = {}
    for name in test_names:
        result[name] = list(filter(lambda line: name in line, lines))
    return result

def __parse_results(results_dict: dict) -> dict:
    parsed = {}
    for test, results in results_dict.items():
        per_metric = {}
        for result in results:
            metric, values = __parse_single_result(result)
            per_metric[metric] = values
        parsed[test] = per_metric
    return parsed

def __parse_startup_results(results_dict: dict) -> float | None:
    parsed = __parse_results(results_dict)[STARTUP].get(STARTUP_TIME_S)
    if parsed == None: return None
    return parsed[0] if len(parsed) > 0 else None

def __parse_single_result(result: str) -> tuple | None:
    if CPU_CYCLES_KC in result: key = CPU_CYCLES_KC
    elif ABSOLUTE_MEMORY_KB in result: key = ABSOLUTE_MEMORY_KB
    elif STARTUP_TIME_S in result: key = STARTUP_TIME_S
    else: return None
    values_start = result.index(__VALUES_KEY) + len(__VALUES_KEY)
    values_end = None
    for i in range(values_start, len(result)+1):
        if result[i] == ']':
            values_end = i
            break
    if values_end == None: return None
    values_string = result[values_start:values_end+1]
    values = json.loads(values_string)
    return (key, values)

if __name__ == '__main__':
    main()
