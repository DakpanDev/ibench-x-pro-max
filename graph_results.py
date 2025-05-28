import sys
from plotting.graphs import *
from save_results import *
from utils import parse_parameters

__REGULAR_PACKAGE = 'Regular'
__SHARED_PACKAGE = 'KMP'
__REGULAR_VERSION = 'Regular Version'
__SHARED_VERSION = 'KMP Version'
__FLOWS = [LOAD_FLIGHTS, OPEN_DETAILS, BOOKMARK_FLIGHT, LOAD_BOOKMARS]

class GraphingConfig:
    def __init__(self, cpu: bool, memory: bool, startup: bool):
        self.cpu = cpu
        self.memory = memory
        self.startup = startup

def main(config: GraphingConfig):
    if config.cpu: __plot_cpu()
    if config.memory: __plot_memory()
    if config.startup: __plot_startup()

def __plot_cpu():
    regular_path = create_path(__REGULAR_PACKAGE)
    shared_path = create_path(__SHARED_PACKAGE)
    regular_plots = [__read_boxplot(regular_path, CPU_USAGE_FILENAME, flow, __REGULAR_VERSION) for flow in __FLOWS]
    shared_plots = [__read_boxplot(shared_path, CPU_USAGE_FILENAME, flow, __SHARED_VERSION) for flow in __FLOWS]
    for regular, shared, flow in zip(regular_plots, shared_plots, __FLOWS):
        plot_regular_boxplot([regular, shared], f'{CPU_USAGE_FIELDNAME}: {flow}')

def __plot_memory():
    regular_path = create_path(__REGULAR_PACKAGE)
    shared_path = create_path(__SHARED_PACKAGE)
    regular_plots = [__read_boxplot(regular_path, MEMORY_USAGE_FILENAME, flow, __REGULAR_VERSION) for flow in __FLOWS]
    shared_plots = [__read_boxplot(shared_path, MEMORY_USAGE_FILENAME, flow, __SHARED_VERSION) for flow in __FLOWS]
    for regular, shared, flow in zip(regular_plots, shared_plots, __FLOWS):
        plot_regular_boxplot([regular, shared], f'{MEMORY_USAGE_FIELDNAME}: {flow}')

def __plot_startup():
    regular_path = create_path(__REGULAR_PACKAGE)
    shared_path = create_path(__SHARED_PACKAGE)
    regular_plot = __read_boxplot(regular_path, STARTUP_TIMES_FILENAME, STARTUP_TIMES_FIELDNAME, __REGULAR_VERSION)
    shared_plot = __read_boxplot(shared_path, STARTUP_TIMES_FILENAME, STARTUP_TIMES_FIELDNAME, __SHARED_VERSION)
    plots = list(filter(lambda x: x != None, [regular_plot, shared_plot]))
    plot_regular_boxplot(plots, STARTUP_TIMES_FIELDNAME)

def __read_boxplot(path: str, filename: str, fieldname: str, title: str) -> BoxPlot | None:
    try:
        with open(f'{path}/{filename}', mode='r') as file:
            reader = csv.DictReader(file)
            return BoxPlot(
                values=[float(row[fieldname]) for row in reader],
                title=title,
            )
    except Exception as error:
        print(error)
        return None

if __name__ == '__main__':
    args = parse_parameters(sys.argv)
    config = GraphingConfig(
        cpu=args['cpu'],
        memory=args['memory'],
        startup=args['startup'],
    )
    main(config)
