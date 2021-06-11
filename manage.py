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

    subparsers = parser.add_subparsers(help="supported commands")

    runserver_parser = subparsers.add_parser("runserver",
                                             help="Run a local HUME "
                                                  "development server.")
    runserver_parser.add_argument("hume_uuid",
                                  type=str,
                                  help="UUID for the HUME instance")
    runserver_parser.add_argument("-t-rds",
                                  "--test-run-device-simulator",
                                  help="Run a device simulator alongside DC.",
                                  action='store_true')
    runserver_parser.set_defaults(func=run_dev_server)

    return parser.parse_args()


def run_dev_server(runserver_args):

    def start_dc(args):
        optional_args = []
        optional_args.append("--t-rds") if args.test_run_device_simulator \
            else None

        base_cmd = ["python", "dc/main.py", args.hume_uuid]
        base_cmd.extend(optional_args)
        subprocess.run(base_cmd)

    def start_hc(args):
        optional_args = []

        base_cmd = ["python", "hc/main.py", args.hume_uuid]
        base_cmd.extend(optional_args)
        subprocess.run(base_cmd)

    dc_thread = threading.Thread(target=start_dc,
                                 args=(runserver_args,))
    hc_thread = threading.Thread(target=start_hc,
                                 args=(runserver_args,))
    dc_thread.start()
    hc_thread.start()
    threading.Event().wait()


cli_args = parse_args()
print(cli_args)
cli_args.func(cli_args)
