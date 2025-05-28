class BenchmarkConfig:
    def __init__(self, platform: str, n: int, package: str, profile: dict, load_flights: bool, 
                 open_details: bool, bookmark_flight: bool, load_bookmarks: bool, 
                 measure_startup: bool, measure_framerate: bool):
        self.platform = platform
        self.package = package
        self.n = n
        self.profile = profile
        self.load_flights = load_flights
        self.open_details = open_details
        self.bookmark_flight = bookmark_flight
        self.load_bookmarks = load_bookmarks
        self.measure_startup = measure_startup
        self.measure_framerate = measure_framerate
