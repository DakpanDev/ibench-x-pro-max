PLATFORM_ANDROID = 'android'
PLATFORM_IOS = 'ios'

__arguments = {
    'cpu': False,       # Plot CPU usage
    'memory': False,    # Plot memory usage
    'startup': False,   # Plot startup time
    'framerate': False, # Plot framerate
}

def parse_parameters(args: list[str]) -> dict:
    parsed = __arguments
    for index, arg in enumerate(args):
        if arg[0] != '-':
            continue
        if arg[1] == '-':
            parsed[arg[2:]] = True
            continue
        parsed[arg[1:]] = args[index+1]
    return parsed
