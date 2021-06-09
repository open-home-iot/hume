#! python

import subprocess
import argparse
import threading


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


def start_dc(hume_uuid):
    subprocess.run([
        "python", "dc/main.py", hume_uuid, "--test-run-device-simulator"
    ])


def start_hc(hume_uuid):
    subprocess.run([
        "python", "hc/main.py", hume_uuid
    ])


args = parse_args()
dc_thread = threading.Thread(target=start_dc, args=(args.hume_uuid, ))
hc_thread = threading.Thread(target=start_hc, args=(args.hume_uuid, ))
dc_thread.start()
hc_thread.start()
threading.Event().wait()
