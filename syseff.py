import psutil

from datetime import datetime
from enum import Enum


line_width = 100

class SysInfoType(Enum):
    CPU = 0
    RAM = 1
    DISK = 2
    NET = 3
    OTHER = 4


class SystemEfficiency:
    def __init__(self) -> None:
        self.cpu = psutil.cpu_times_percent(interval=1)
        self.vir_mem = psutil.virtual_memory()
        self.swap_mem = psutil.swap_memory()
        self.disk = psutil.disk_io_counters()
        self.net = psutil.net_io_counters()
        self.users = psutil.users()
        self.time = psutil.boot_time()

        self.cpu_banner = "CPU Efficiency Information"
        self.cpu_info = [
            ("Name", "Value"),
            ("user_time", str(self.cpu.user) + "%"),
            ("sys_time", str(self.cpu.system) + "%"),
            # ("wait_io", str(self.cpu.iowait) + "%"),
            ("idle", str(self.cpu.idle) + "%")
        ]

        self.ram_banner = "Ram Efficiency Information"
        self.ram_info = [
            ("Name", "Value"),
            ("total", giga_bytes(self.vir_mem.total)),
            ("used", giga_bytes(self.vir_mem.used)),
            ("free", million_bytes(self.vir_mem.free)),
            # ("buffers", million_bytes(self.vir_mem.buffers)),
            # ("cached", million_bytes(self.vir_mem.cached)),
            ("swap_used", million_bytes(self.swap_mem.used))
        ]
        
        self.disk_banner = "Disk Efficiency Information"
        self.disk_info = [
            ("name", "value"),
            ("read_count", str(self.disk.read_count)),
            ("write_count", str(self.disk.write_count)),
            ("read_bytesio", giga_bytes(self.disk.read_bytes)),
            ("write_bytesio", giga_bytes(self.disk.write_bytes)),
            ("read_time", str(self.disk.read_time)),
            ("write_time", str(self.disk.write_time))
        ]

        self.net_banner = "Net Efficiency Information"
        self.net_info = [
            ("name", "value"),
            ("bytes_sent", million_bytes(self.net.bytes_sent)),
            ("bytes_recv", million_bytes(self.net.bytes_recv)),
            ("packets_sent", str(self.net.packets_sent)),
            ("packets_recv", str(self.net.packets_recv))
        ]

        self.other_banner = "Other Information"
        self.other_info = [
            ("name", "value"),
            ("time", datetime.fromtimestamp(self.time).strftime("%Y-%m-%d %H:%M:%S"))
        ] + [("user_name", user.name) for user in self.users]


    def format_to_file(self, file_path: str, type: SysInfoType, mode="w"):
        match type:
            case SysInfoType.CPU:
                banner = self.cpu_banner
                info = self.cpu_info
            case SysInfoType.RAM:
                banner = self.ram_banner
                info = self.ram_info
            case SysInfoType.DISK:
                banner = self.disk_banner
                info = self.disk_info
            case SysInfoType.NET:
                banner = self.net_banner
                info = self.net_info
            case SysInfoType.OTHER:
                banner = self.other_banner
                info = self.other_info
        with open(file_path, mode, encoding="UTF-8") as file:
            file.write(gen_cell_line([banner], line_width))
            for i in info:
                file.write(gen_cell_line([i[0], i[1]], line_width))
            file.write(gen_end_line(2, line_width))


def giga_bytes(bytes: int) -> str:
    return "{:.2f} GB".format(bytes / (1024 * 1024 * 1024))

def million_bytes(bytes: int) -> str:
    return "{:.2f} MB".format(bytes / (1024 * 1024))

def kilo_bytes(bytes: int) -> str:
    return "{:.2f} KB".format(bytes / 1024)

def gen_end_line(items_len: int, width: int) -> str:
    cell_space = width - items_len - 1
    avg_space =  cell_space // items_len
    last_space = avg_space + cell_space % avg_space
    return "+" + ("-" * avg_space + "+") * (items_len - 1) + "-" * (last_space) + "+\n"\

def gen_cell_line(items: list, width: int) -> str:
    cell_space = width - len(items) - 1
    avg_space =  cell_space // len(items)
    last_space = avg_space + cell_space % avg_space
    return "+" + ("-" * avg_space + "+") * (len(items) - 1) + "-" * (last_space) + "+\n"\
            "|" + ''.join([str(item).center(avg_space) + "|" for item in items][:-1]) + str(items[-1]).center(last_space) + "|\n"
