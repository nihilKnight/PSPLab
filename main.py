from sys_info import SysInfoType, SystemInfo


output_path = "outputs/sys_info.txt"

if __name__ == "__main__":
    se = SystemInfo()
    se.format_to_file(output_path, SysInfoType.CPU)
    se.format_to_file(output_path, SysInfoType.RAM, "a")
    se.format_to_file(output_path, SysInfoType.DISK, "a")
    se.format_to_file(output_path, SysInfoType.NET, "a")
    se.format_to_file(output_path, SysInfoType.OTHER, "a")

