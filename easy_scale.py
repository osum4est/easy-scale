import subprocess
from math import sqrt


class Monitor:
    def __init__(self, input: str):
        parts = input.split(",")
        res_parts = parts[1].split("@")
        self.name: str = parts[0]
        self.resolution: tuple[int, int] = (int(res_parts[0].split("x")[0]), int(res_parts[0].split("x")[1]))
        self.rate: float = float(res_parts[1])
        self.diagonal_inch: float = float(parts[2])


def run(args):
    monitors = [Monitor(m) for m in args.monitors]
    scale = 1 / (args.scale / 100)
    primary = get_monitor(args.primary, monitors)

    if args.dpi is not None:
        dpi = args.dpi
    else:
        lowest = min(monitors, key=lambda m: m.resolution[0] * m.resolution[1])
        dpi = round(get_dpi(lowest) * 2 * (args.scale / 100), 3)

    x = 0
    xrandr = ""
    xrandr += "xrandr "
    for monitor in monitors:
        monitor_dpi = get_dpi(monitor)
        monitor_scale = round((dpi / monitor_dpi) * scale, 3)
        xrandr += f" --output {monitor.name}"
        xrandr += f" --mode {monitor.resolution[0]}x{monitor.resolution[1]}"
        xrandr += f" --rate {monitor.rate}"
        xrandr += f" --scale {monitor_scale}"
        xrandr += f" --pos {x}x0"

        if primary.name == monitor.name:
            xrandr += " --primary"

        x += int(monitor.resolution[0] * monitor_scale) + 1

    xrdb = f"echo \"Xft.dpi: {dpi}\" | xrdb -merge"
    print(xrandr)
    print("")
    print(xrdb)


def get_monitor(name: str, monitors: list[Monitor]):
    return next((m for m in monitors if m.name == name))


def get_dpi(monitor: Monitor) -> float:
    diagonal_res = sqrt(monitor.resolution[0] ** 2 + monitor.resolution[1] ** 2)
    width = monitor.diagonal_inch * (monitor.resolution[0] / diagonal_res)
    return monitor.resolution[0] / width
