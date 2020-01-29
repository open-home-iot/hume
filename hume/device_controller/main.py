import argparse

from root_app.root import RootApp


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(description="HUME device controller")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    root_app = RootApp(cli_args=args)
    root_app.start()

    # To block on start to test
    inp = input()
