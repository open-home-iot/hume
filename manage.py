#! python

import subprocess
import argparse


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(
        description="HUME device controller"
    )

    # HUME identification
    parser.add_argument('hume_uuid',
                        metavar="HUME_UUID",
                        help="HUME UUID")

    return parser.parse_args()


args = parse_args()

subprocess.run([
    "python", "dc/main.py", args.hume_uuid
])
subprocess.run([
    "python", "hc/main.py", args.hume_uuid
])
