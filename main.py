import argparse

from scanner import Scanner


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="webScanner")
    parser.add_argument("-T", "--targets", nargs="+", required=True, help="targets for scanning, format as \"http(s)://example.com/\"")
    parser.add_argument("-D", "--dynamic-mode", action="store_true", help="enable dynamic crawling mode.")
    parser.add_argument("-t", "--threads", action="store", type=int, default=128, help="the threads used for scanning. Default to be 128.")
    parser.add_argument("-d", "--depth", action="store", type=int, default=3, help="recursive depth when enabling dynamic mode. Default to be 3.")

    args = parser.parse_args()

    Scanner(targets=args.targets, is_dyn=args.dynamic_mode, threads=args.threads, dynamic_depth=args.depth).scan()

