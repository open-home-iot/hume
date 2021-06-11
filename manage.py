#! python

import subprocess
import argparse
import threading

import peewee

from dc.device.models import Device
from hc.hint.models import BrokerCredentials, HumeUser


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(
        description="HUME device controller"
    )

    parser.add_argument("-cdb",
                        "--clean-db",
                        action="store_true",
                        help="Clean all tables in local Postgres DB 'hume'")

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


def clean_db():
    """
    Clean the local Postgres DB 'hume' of all table content. If new tables are
    added to HUME, they must be added here as well, I don't have the energy for
    fixing automatic discovery.
    """
    print("clearing the local Postgres DB 'hume' of all tables...\n")

    psql_db = peewee.PostgresqlDatabase("hume",
                                        user="hume",
                                        password="password")
    psql_db.connect()
    psql_db.drop_tables([Device, BrokerCredentials, HumeUser])


"""
Subparsers below
"""


def run_dev_server(runserver_args):
    """
    Runs a local development server for HUME, starting both HC and DC.

    :param runserver_args: arguments for the 'runserver' command
    """
    print("starting HUME development server...\n")

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


if __name__ == "__main__":
    cli_args = parse_args()
    if cli_args.clean_db:
        clean_db()
    cli_args.func(cli_args)
