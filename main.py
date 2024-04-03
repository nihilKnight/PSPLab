from syseff import SysInfoType, SystemEfficiency


output_path = "outputs/syseff.txt"

if __name__ == "__main__":
    se = SystemEfficiency()
    se.format_to_file(output_path, SysInfoType.CPU)
    se.format_to_file(output_path, SysInfoType.RAM, "a")
    se.format_to_file(output_path, SysInfoType.DISK, "a")
    se.format_to_file(output_path, SysInfoType.NET, "a")
    se.format_to_file(output_path, SysInfoType.OTHER, "a")

