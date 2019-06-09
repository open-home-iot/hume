import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser(description='HUME, the HOME network hub')

    # parser.add_argument('--serial_port', type=str, required=True)
    # parser.add_argument('--baudrate', type=int)
    # parser.add_argument('--ip', type=str)
    # parser.add_argument('--port', type=int)
    args = arg_parser.parse_args()
    print(args)
