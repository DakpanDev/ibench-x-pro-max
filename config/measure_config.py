class MeasureConfig:
    def __init__(self, platform: str, package: str, measure_cpu: bool, measure_memory: bool, 
                 measure_battery: bool, measure_app_size: bool):
        self.platform = platform
        self.package = package
        self.measure_cpu = measure_cpu
        self.measure_memory = measure_memory
        self.measure_battery = measure_battery
        self.measure_app_size = measure_app_size
