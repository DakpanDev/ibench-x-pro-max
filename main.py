import os
import json
import pprint

# Command Building
__START_TEST_COMMAND = 'xcodebuild test'
__SCHEME_ARG = '-scheme MyTerminal'
__PROJECT_ARG = '-project'
__DESTINATION_ARG = '-destination'
__TESTING_ARG = '-only-testing:MyTerminalUITests/MyTerminalUITests'

# Test names
__LOAD_FLIGHTS = 'LoadFlights'
__OPEN_DETAILS = 'OpenDetails'
__BOOKMARK_FLIGHT = 'BookmarkFlight'
__LOAD_BOOKMARS = 'LoadBookmarks'

# Relevant metrics
__CPU_CYCLES_KC = 'CPU Cycles'
__ABSOLUTE_MEMORY_KB = 'Absolute Memory Physical'
__STARTUP_TIME_S = 'Duration'

# Other
__VALUES_KEY = 'values: '

def main():
    project_path = '/Users/mitchell.tol/Projects/MyTerminal/iOS/myterminal-ios'
    device_id = '00008101-001D04260190001E'
    destination = f'\'id={device_id}\''
    metrics_stream = os.popen(f'{__START_TEST_COMMAND} {__SCHEME_ARG} {__PROJECT_ARG} {project_path}/MyTerminal.xcodeproj ' + 
             f'{__DESTINATION_ARG} {destination} {__TESTING_ARG} | grep "{project_path}" | grep "Test Case" ' + 
             f'| grep -e "{__CPU_CYCLES_KC}" -e "{__ABSOLUTE_MEMORY_KB}" -e "{__STARTUP_TIME_S}"').read()
    metrics_lines = metrics_stream.splitlines()
    grouped = __group_results(metrics_lines, [__LOAD_FLIGHTS, __OPEN_DETAILS, __BOOKMARK_FLIGHT, __LOAD_BOOKMARS])
    parsed = __parse_results(grouped)
    pprint.pp(parsed)

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

def __parse_single_result(result: str) -> tuple | None:
    if __CPU_CYCLES_KC in result: key = __CPU_CYCLES_KC
    elif __ABSOLUTE_MEMORY_KB in result: key = __ABSOLUTE_MEMORY_KB
    elif __STARTUP_TIME_S in result: key = __STARTUP_TIME_S
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
